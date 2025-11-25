import streamlit as st
import google.generativeai as genai
import json

# Page configuration
st.set_page_config(
    page_title="QA Edge Case Generator",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("🔍 QA Edge Case Generator")
st.markdown("Generate comprehensive test scenarios for your features using AI")

# Sample scenarios for demo mode
DEMO_SCENARIOS = {
    "Functional": [
        "Test user login with valid credentials and verify successful authentication",
        "Verify 'Remember Me' functionality persists login state across browser sessions",
        "Test 'Forgot Password' link redirects to password recovery page",
        "Verify login fails with incorrect password and displays appropriate error message",
        "Test session timeout after 30 days when 'Remember Me' is enabled",
        "Verify multiple failed login attempts trigger account lockout mechanism"
    ],
    "Security": [
        "Test SQL injection attempts in email and password fields",
        "Verify password is not visible in plain text or network requests",
        "Test brute force attack prevention with rate limiting",
        "Verify session tokens are properly encrypted and invalidated on logout",
        "Test XSS (Cross-Site Scripting) vulnerabilities in input fields",
        "Verify CSRF token validation for login form submission"
    ],
    "Input Validation": [
        "Test login with empty email and password fields",
        "Verify email format validation (invalid formats: no @, missing domain, etc.)",
        "Test password field with special characters, emojis, and unicode",
        "Verify maximum length limits for email and password fields",
        "Test login with SQL/script injection payloads in input fields",
        "Verify whitespace handling (leading/trailing spaces in credentials)"
    ],
    "Network": [
        "Test login behavior when network connection is lost mid-request",
        "Verify timeout handling for slow API responses (>30 seconds)",
        "Test login with intermittent network connectivity",
        "Verify proper error handling when authentication server is down",
        "Test behavior with very slow network speeds (3G/Edge simulation)",
        "Verify retry mechanism for failed network requests"
    ]
}

# Initialize Gemini client
@st.cache_resource
def get_gemini_model():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.5-pro')
    except Exception as e:
        return None

model = get_gemini_model()

# Main input area
st.markdown("### 기획 기능 설명 (Feature Description)")
feature_description = st.text_area(
    label="기획 기능 설명 (Feature Description)",
    label_visibility="collapsed",
    placeholder="Enter your feature description here...\n\nExample: A login form that accepts email and password, with a 'Remember Me' checkbox and 'Forgot Password' link.",
    height=200
)

# Generate button
if st.button("🚀 시나리오 생성 (Generate Scenarios)", type="primary", use_container_width=True):
    if not feature_description.strip():
        st.warning("Please enter a feature description first.")
    elif not model:
        # Demo mode - use sample scenarios
        st.info("🎭 **Demo Mode**: Using sample test scenarios (Gemini API key not configured)")
        st.markdown("*To use AI-powered generation, add your Gemini API key to `.streamlit/secrets.toml`*")
        
        with st.spinner("Loading demo scenarios..."):
            import time
            time.sleep(1)  # Simulate processing
            
            scenarios = DEMO_SCENARIOS
            
            # Display results
            st.success("✅ Demo test scenarios loaded successfully!")
            st.markdown("---")
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            # Functional scenarios
            with col1:
                st.markdown("### 🎯 Functional")
                for i, scenario in enumerate(scenarios.get("Functional", []), 1):
                    st.markdown(f"{i}. {scenario}")
                st.markdown("")
            
            # Security scenarios
            with col2:
                st.markdown("### 🔒 Security")
                for i, scenario in enumerate(scenarios.get("Security", []), 1):
                    st.markdown(f"{i}. {scenario}")
                st.markdown("")
            
            # Input Validation scenarios
            with col1:
                st.markdown("### ✅ Input Validation")
                for i, scenario in enumerate(scenarios.get("Input Validation", []), 1):
                    st.markdown(f"{i}. {scenario}")
                st.markdown("")
            
            # Network scenarios
            with col2:
                st.markdown("### 🌐 Network")
                for i, scenario in enumerate(scenarios.get("Network", []), 1):
                    st.markdown(f"{i}. {scenario}")
    else:
        # AI mode - use Gemini API
        with st.spinner("Generating test scenarios with AI..."):
            try:
                # Create the prompt for Gemini
                prompt = f"""You are a QA expert. Given the following feature description, generate comprehensive edge case test scenarios.

Feature Description:
{feature_description}

Please generate test scenarios in the following 4 categories:
1. Functional - Core functionality and business logic edge cases
2. Security - Security vulnerabilities and attack vectors
3. Input Validation - Invalid inputs, boundary conditions, data type issues
4. Network - Network-related issues, timeouts, connectivity problems

For each category, provide 5-7 specific test scenarios. Format your response as a JSON object with the following structure:
{{
    "Functional": ["scenario 1", "scenario 2", ...],
    "Security": ["scenario 1", "scenario 2", ...],
    "Input Validation": ["scenario 1", "scenario 2", ...],
    "Network": ["scenario 1", "scenario 2", ...]
}}

Only return the JSON object, no additional text."""

                # Call Gemini API
                response = model.generate_content(prompt)
                result_text = response.text.strip()
                
                # Remove markdown code blocks if present
                if result_text.startswith("```json"):
                    result_text = result_text[7:]
                if result_text.startswith("```"):
                    result_text = result_text[3:]
                if result_text.endswith("```"):
                    result_text = result_text[:-3]
                result_text = result_text.strip()
                
                scenarios = json.loads(result_text)
                
                # Display results
                st.success("✅ Test scenarios generated successfully!")
                st.markdown("---")
                
                # Create columns for better layout
                col1, col2 = st.columns(2)
                
                # Functional scenarios
                with col1:
                    st.markdown("### 🎯 Functional")
                    for i, scenario in enumerate(scenarios.get("Functional", []), 1):
                        st.markdown(f"{i}. {scenario}")
                    st.markdown("")
                
                # Security scenarios
                with col2:
                    st.markdown("### 🔒 Security")
                    for i, scenario in enumerate(scenarios.get("Security", []), 1):
                        st.markdown(f"{i}. {scenario}")
                    st.markdown("")
                
                # Input Validation scenarios
                with col1:
                    st.markdown("### ✅ Input Validation")
                    for i, scenario in enumerate(scenarios.get("Input Validation", []), 1):
                        st.markdown(f"{i}. {scenario}")
                    st.markdown("")
                
                # Network scenarios
                with col2:
                    st.markdown("### 🌐 Network")
                    for i, scenario in enumerate(scenarios.get("Network", []), 1):
                        st.markdown(f"{i}. {scenario}")
                
            except json.JSONDecodeError as e:
                st.error(f"Error parsing API response: {e}")
                st.code(result_text)
            except Exception as e:
                st.error(f"Error generating scenarios: {e}")
                st.info("Please check your API key and try again.")

# Sidebar with instructions
with st.sidebar:
    st.markdown("## 📖 How to Use")
    st.markdown("""
    1. Enter your feature description in the text area
    2. Click the 'Generate Scenarios' button
    3. Review the generated test scenarios across 4 categories
    
    **Categories:**
    - 🎯 **Functional**: Core functionality tests
    - 🔒 **Security**: Security vulnerability tests
    - ✅ **Input Validation**: Data validation tests
    - 🌐 **Network**: Network-related tests
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuration")
    if model:
        st.markdown("🤖 **Mode**: AI-Powered (Gemini Pro)")
        st.markdown("API Key: ✅ Configured")
    else:
        st.markdown("🎭 **Mode**: Demo Mode")
        st.markdown("API Key: ❌ Not configured")
        st.info("App works in demo mode with sample scenarios. Configure API key for AI-powered generation.")

