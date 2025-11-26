"""
Shared configuration module for QA Edge Case Generator.
Loads Gemini API key from Streamlit secrets or environment variables.
"""
import os
import toml

def get_gemini_api_key():
    """
    Get Gemini API key from Streamlit secrets or environment variable.
    
    Returns:
        str: Gemini API key or None if not found
    """
    # Try to load from Streamlit secrets
    try:
        secrets_path = os.path.join(os.path.dirname(__file__), '.streamlit', 'secrets.toml')
        if os.path.exists(secrets_path):
            secrets = toml.load(secrets_path)
            return secrets.get('GEMINI_API_KEY')
    except Exception as e:
        print(f"Warning: Could not load from secrets.toml: {e}")
    
    # Fallback to environment variable
    return os.environ.get('GEMINI_API_KEY')
