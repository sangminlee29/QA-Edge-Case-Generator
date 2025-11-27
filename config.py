"""
Shared configuration module for QA Edge Case Generator.
Supports both Gemini API Key and Vertex AI with automatic switching.
"""
import os
import toml
from typing import Optional, Dict, Any

def get_api_config() -> Dict[str, Any]:
    """
    Get API configuration from Streamlit secrets or environment variables.
    Supports both Gemini API Key and Vertex AI.
    
    Returns:
        dict: Configuration dict with 'api_type' and relevant credentials
              - api_type: 'gemini' or 'vertex'
              - For Gemini: 'api_key'
              - For Vertex: 'project_id', 'location', 'credentials_path' (optional)
    """
    config = {}
    
    # Try to load from Streamlit secrets
    try:
        secrets_path = os.path.join(os.path.dirname(__file__), '.streamlit', 'secrets.toml')
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            
            # Check which API type to use (default: gemini)
            api_type = secrets.get('API_TYPE', 'gemini').lower()
            config['api_type'] = api_type
            
            if api_type == 'gemini':
                # Gemini API Key configuration
                config['api_key'] = secrets.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY')
            elif api_type == 'vertex':
                # Vertex AI configuration
                config['project_id'] = secrets.get('VERTEX_AI_PROJECT_ID') or os.environ.get('VERTEX_AI_PROJECT_ID')
                config['location'] = secrets.get('VERTEX_AI_LOCATION') or os.environ.get('VERTEX_AI_LOCATION', 'us-central1')
                config['credentials_path'] = secrets.get('VERTEX_AI_CREDENTIALS_PATH') or os.environ.get('VERTEX_AI_CREDENTIALS_PATH')
                config['credentials_json'] = secrets.get('VERTEX_AI_CREDENTIALS_JSON') or os.environ.get('VERTEX_AI_CREDENTIALS_JSON')
                config['model_name'] = secrets.get('VERTEX_AI_MODEL', 'gemini-2.5-pro')
            else:
                raise ValueError(f"Unknown API_TYPE: {api_type}. Must be 'gemini' or 'vertex'")
            
            return config
    except Exception as e:
        print(f"Warning: Could not load from secrets.toml: {e}")
    
    # Fallback: Try environment variables
    if os.environ.get('GEMINI_API_KEY'):
        return {
            'api_type': 'gemini',
            'api_key': os.environ.get('GEMINI_API_KEY')
        }
    
    return config

def get_gemini_api_key():
    """
    Get Gemini API key (backward compatibility).
    
    Returns:
        str: Gemini API key or None if not found
    """
    config = get_api_config()
    if config.get('api_type') == 'gemini':
        return config.get('api_key')
    return None

def get_ai_model():
    """
    Initialize and return AI model based on configuration.
    Supports both Gemini API Key and Vertex AI.
    
    Returns:
        Model object (Gemini or Vertex AI) or None if configuration is invalid
    """
    config = get_api_config()
    
    if not config:
        print("Warning: No API configuration found")
        return None
    
    api_type = config.get('api_type', 'gemini')
    
    try:
        if api_type == 'gemini':
            # Use Gemini API Key
            import google.generativeai as genai
            api_key = config.get('api_key')
            if not api_key:
                print("Warning: GEMINI_API_KEY not found")
                return None
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-pro')
            print("✅ Gemini API initialized successfully")
            return model
            
        elif api_type == 'vertex':
            # Use Vertex AI
            import vertexai
            from vertexai.generative_models import GenerativeModel
            from google.oauth2 import service_account
            
            project_id = config.get('project_id')
            location = config.get('location', 'us-central1')
            credentials_path = config.get('credentials_path')
            credentials_json = config.get('credentials_json')  # JSON string from secrets.toml
            model_name = config.get('model_name', 'gemini-3-pro-preview')
            
            if not project_id:
                print("Warning: VERTEX_AI_PROJECT_ID not found")
                return None
            
            # Load credentials - priority: JSON string > file path > Application Default Credentials
            credentials = None
            if credentials_json:
                # Load from JSON string in secrets.toml
                try:
                    import json as json_lib
                    creds_dict = json_lib.loads(credentials_json)
                    credentials = service_account.Credentials.from_service_account_info(
                        creds_dict,
                        scopes=['https://www.googleapis.com/auth/cloud-platform']
                    )
                    print("✅ Credentials loaded from secrets.toml (JSON)")
                except Exception as e:
                    print(f"Warning: Failed to load credentials from JSON: {e}")
                    credentials = None
            elif credentials_path and os.path.exists(credentials_path):
                # Load from file path (backward compatibility)
                credentials = service_account.Credentials.from_service_account_file(
                    credentials_path,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
                print(f"✅ Credentials loaded from file: {credentials_path}")
            
            # Initialize Vertex AI
            if credentials:
                vertexai.init(
                    project=project_id,
                    location=location,
                    credentials=credentials
                )
            else:
                vertexai.init(project=project_id, location=location)
            
            model = GenerativeModel(model_name)
            print(f"✅ Vertex AI initialized successfully (project: {project_id}, location: {location})")
            return model
            
        else:
            print(f"Warning: Unknown API type: {api_type}")
            return None
            
    except ImportError as e:
        print(f"Error: Required package not installed: {e}")
        if api_type == 'vertex':
            print("Install with: pip install google-cloud-aiplatform")
        return None
    except Exception as e:
        print(f"Error initializing AI model: {e}")
        import traceback
        print(traceback.format_exc())
        return None

def get_generation_config(response_mime_type: Optional[str] = None, temperature: float = 0.7):
    """
    Get generation config for the configured API type.
    
    Args:
        response_mime_type: MIME type for response (e.g., 'application/json')
        temperature: Temperature for generation (default: 0.7)
    
    Returns:
        GenerationConfig object compatible with the configured API
    """
    config = get_api_config()
    api_type = config.get('api_type', 'gemini')
    
    if api_type == 'gemini':
        import google.generativeai as genai
        kwargs = {'temperature': temperature}
        if response_mime_type:
            kwargs['response_mime_type'] = response_mime_type
        return genai.GenerationConfig(**kwargs)
    else:  # vertex
        from vertexai.generative_models import GenerationConfig
        kwargs = {'temperature': temperature}
        if response_mime_type:
            kwargs['response_mime_type'] = response_mime_type
        return GenerationConfig(**kwargs)
