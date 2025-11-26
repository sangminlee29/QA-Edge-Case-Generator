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
        {
            "title": "유효한 자격 증명으로 로그인 테스트",
            "description": "올바른 이메일과 비밀번호를 입력했을 때 사용자가 성공적으로 인증되고 대시보드로 리디렉션되는지 확인. 세션 토큰이 올바르게 생성되는지 검증.",
            "severity": "High"
        },
        {
            "title": "'로그인 상태 유지' 기능 영속성 검증",
            "description": "브라우저를 닫고 다시 열었을 때 로그인 상태가 유지되는지 확인. 쿠키 만료 시간이 30일로 설정되어 있는지 검증.",
            "severity": "Medium"
        },
        {
            "title": "잘못된 비밀번호 입력 시 에러 처리",
            "description": "올바른 이메일에 잘못된 비밀번호를 입력했을 때 적절한 에러 메시지가 표시되고, 보안상 이유로 어떤 필드가 틀렸는지 명시하지 않는지 확인.",
            "severity": "High"
        },
        {
            "title": "30일 후 세션 타임아웃 테스트",
            "description": "'로그인 상태 유지'가 활성화된 상태에서 정확히 30일 후 세션이 만료되는지 확인. 만료 후 재로그인이 필요한지 검증.",
            "severity": "Low"
        },
        {
            "title": "다중 로그인 실패 시 계정 잠금",
            "description": "5회 연속 로그인 실패 시 계정이 일시적으로 잠기는지 확인. 잠금 해제 메커니즘(이메일 인증, 시간 기반)이 작동하는지 검증.",
            "severity": "High"
        }
    ],
    "Security": [
        {
            "title": "SQL 인젝션 공격 방어",
            "description": "이메일과 비밀번호 필드에 SQL 인젝션 페이로드(예: ' OR '1'='1)를 입력했을 때 적절히 이스케이프되고 공격이 차단되는지 확인.",
            "severity": "High"
        },
        {
            "title": "비밀번호 평문 노출 방지",
            "description": "네트워크 요청에서 비밀번호가 평문으로 전송되지 않는지 확인. HTTPS 사용 및 요청 본문 암호화 검증.",
            "severity": "High"
        },
        {
            "title": "무차별 대입 공격 방지",
            "description": "짧은 시간 내 다수의 로그인 시도 시 rate limiting이 작동하는지 확인. IP 기반 또는 계정 기반 제한이 적용되는지 검증.",
            "severity": "High"
        },
        {
            "title": "세션 토큰 암호화 및 무효화",
            "description": "로그아웃 시 세션 토큰이 서버에서 완전히 무효화되는지 확인. 이전 토큰으로 재접근 시도 시 거부되는지 검증.",
            "severity": "High"
        },
        {
            "title": "XSS 취약점 테스트",
            "description": "입력 필드에 스크립트 태그(<script>alert('XSS')</script>)를 삽입했을 때 적절히 sanitize되고 실행되지 않는지 확인.",
            "severity": "High"
        },
        {
            "title": "CSRF 토큰 검증",
            "description": "로그인 폼 제출 시 CSRF 토큰이 포함되어 있고, 유효하지 않은 토큰으로 요청 시 거부되는지 확인.",
            "severity": "Medium"
        }
    ],
    "Input Validation": [
        {
            "title": "빈 필드 입력 검증",
            "description": "이메일 또는 비밀번호 필드가 비어있을 때 적절한 유효성 검사 메시지가 표시되고 폼 제출이 차단되는지 확인.",
            "severity": "Medium"
        },
        {
            "title": "이메일 형식 유효성 검사",
            "description": "잘못된 이메일 형식(@ 누락, 도메인 없음, 공백 포함 등)을 입력했을 때 클라이언트 및 서버 측에서 검증되는지 확인.",
            "severity": "Medium"
        },
        {
            "title": "특수 문자 및 유니코드 처리",
            "description": "비밀번호 필드에 특수 문자, 이모지, 다국어 문자를 입력했을 때 올바르게 처리되고 저장되는지 확인.",
            "severity": "Low"
        },
        {
            "title": "최대 길이 제한 검증",
            "description": "이메일과 비밀번호 필드에 매우 긴 문자열(예: 10,000자)을 입력했을 때 적절히 제한되고 에러가 발생하지 않는지 확인.",
            "severity": "Medium"
        },
        {
            "title": "공백 문자 처리",
            "description": "이메일 또는 비밀번호 앞뒤에 공백이 있을 때 자동으로 trim되거나 적절한 에러 메시지가 표시되는지 확인.",
            "severity": "Low"
        }
    ],
    "Network": [
        {
            "title": "네트워크 연결 중단 시 처리",
            "description": "로그인 요청 중 네트워크 연결이 끊겼을 때 적절한 에러 메시지가 표시되고 재시도 옵션이 제공되는지 확인.",
            "severity": "Medium"
        },
        {
            "title": "느린 API 응답 타임아웃 처리",
            "description": "인증 서버가 30초 이상 응답하지 않을 때 타임아웃이 발생하고 사용자에게 알림이 표시되는지 확인.",
            "severity": "Medium"
        },
        {
            "title": "간헐적 네트워크 연결 테스트",
            "description": "불안정한 네트워크 환경에서 로그인 시도 시 재시도 로직이 작동하고 최종적으로 성공 또는 명확한 실패 메시지가 표시되는지 확인.",
            "severity": "Low"
        },
        {
            "title": "인증 서버 다운 시 에러 처리",
            "description": "백엔드 인증 서버가 완전히 다운되었을 때 사용자에게 명확한 에러 메시지가 표시되고 앱이 크래시하지 않는지 확인.",
            "severity": "High"
        },
        {
            "title": "저속 네트워크 환경 테스트",
            "description": "3G 또는 Edge 네트워크를 시뮬레이션하여 로그인 프로세스가 완료되는지, 로딩 인디케이터가 표시되는지 확인.",
            "severity": "Low"
        }
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
            
            # Store scenarios in session state
            st.session_state.scenarios = DEMO_SCENARIOS
            st.session_state.scenarios_loaded = True
            
    else:
        # AI mode - use Gemini API
        with st.spinner("Generating test scenarios with AI..."):
            try:
                # Create the enhanced prompt for Gemini with strong persona
                prompt = f"""너는 구글 출신의 20년 차 시니어 QA 엔지니어다. 개발자들이 흔히 놓치는 사소하지만 치명적인 엣지 케이스(Edge Case)를 찾아내는 것이 목표다.

당신의 전문성:
- 20년간 수천 개의 프로덕션 버그를 분석한 경험
- 사용자들이 예상치 못한 방식으로 시스템을 사용하는 패턴 파악
- 경계 조건, 동시성 문제, 보안 취약점을 찾아내는 능력
- 단순한 테스트가 아닌, 실제로 프로덕션에서 발생할 수 있는 치명적인 시나리오 발굴

Feature Description:
{feature_description}

다음 4가지 카테고리에서 각각 5-7개의 엣지 케이스 테스트 시나리오를 생성하라:
1. Functional - 핵심 기능과 비즈니스 로직의 엣지 케이스
2. Security - 보안 취약점과 공격 벡터
3. Input Validation - 잘못된 입력, 경계 조건, 데이터 타입 이슈
4. Network - 네트워크 관련 문제, 타임아웃, 연결 문제

각 시나리오는 다음 형식으로 작성:
- title: 간결한 테스트 케이스 제목 (한 줄)
- description: 구체적인 테스트 방법과 예상 결과 (2-3문장)
- severity: "High" (치명적), "Medium" (중요), "Low" (경미) 중 하나

응답은 반드시 다음 JSON 형식으로만 출력하라 (다른 텍스트 없이):
{{
    "Functional": [
        {{"title": "...", "description": "...", "severity": "High"}},
        ...
    ],
    "Security": [
        {{"title": "...", "description": "...", "severity": "High"}},
        ...
    ],
    "Input Validation": [
        {{"title": "...", "description": "...", "severity": "Medium"}},
        ...
    ],
    "Network": [
        {{"title": "...", "description": "...", "severity": "Medium"}},
        ...
    ]
}}

JSON 객체만 반환하라. 추가 설명이나 마크다운 코드 블록 없이."""

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
                
                # Store scenarios in session state
                st.session_state.scenarios = scenarios
                st.session_state.scenarios_loaded = True
                
            except json.JSONDecodeError as e:
                st.error(f"Error parsing API response: {e}")
                st.code(result_text)
            except Exception as e:
                st.error(f"Error generating scenarios: {e}")
                st.info("Please check your API key and try again.")

# Display scenarios if they exist in session state
if st.session_state.get('scenarios_loaded', False):
    scenarios = st.session_state.get('scenarios', {})
    
    # Display results
    st.success("✅ Test scenarios generated successfully!")
    st.markdown("---")
    
    # Add custom CSS for severity badges
    st.markdown("""
    <style>
    .severity-high {
        background-color: #ff4444;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .severity-medium {
        background-color: #ffaa00;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .severity-low {
        background-color: #00cc66;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for checkboxes if not exists
    if 'checked_scenarios' not in st.session_state:
        st.session_state.checked_scenarios = {}
    
    # Helper function to get severity badge HTML
    def get_severity_badge(severity):
        severity_class = {
            'High': 'severity-high',
            'Medium': 'severity-medium',
            'Low': 'severity-low'
        }.get(severity, 'severity-medium')
        return f'<span class="{severity_class}">{severity}</span>'
    
    # Helper function to display scenarios with checkboxes
    def display_scenario_interactive(scenario, category, index):
        if isinstance(scenario, dict):
            severity = scenario.get('severity', 'Medium')
            title = scenario.get('title', 'Untitled')
            description = scenario.get('description', '')
            
            # Create unique key for checkbox
            checkbox_key = f"{category}_{index}"
            
            # Checkbox for test completion
            checked = st.checkbox(
                f"**{title}**",
                key=checkbox_key,
                value=st.session_state.checked_scenarios.get(checkbox_key, False)
            )
            st.session_state.checked_scenarios[checkbox_key] = checked
            
            # Display severity badge and description
            st.markdown(
                f"{get_severity_badge(severity)} {description}",
                unsafe_allow_html=True
            )
            st.markdown("")
        else:
            # Fallback for old format
            checkbox_key = f"{category}_{index}"
            st.checkbox(scenario, key=checkbox_key)
    
    # Count scenarios by severity
    def count_by_severity(scenarios_list):
        high = medium = low = 0
        for s in scenarios_list:
            if isinstance(s, dict):
                sev = s.get('severity', 'Medium')
                if sev == 'High':
                    high += 1
                elif sev == 'Medium':
                    medium += 1
                else:
                    low += 1
        return high, medium, low
    
    # Display categories with expanders
    categories = [
        ("Functional", "🎯", "핵심 기능과 비즈니스 로직의 엣지 케이스"),
        ("Security", "🔒", "보안 취약점과 공격 벡터"),
        ("Input Validation", "✅", "잘못된 입력, 경계 조건, 데이터 타입 이슈"),
        ("Network", "🌐", "네트워크 관련 문제, 타임아웃, 연결 문제")
    ]
    
    for category_name, emoji, description in categories:
        category_scenarios = scenarios.get(category_name, [])
        if category_scenarios:
            high, medium, low = count_by_severity(category_scenarios)
            
            # Create expander with count badges
            badge_html = ""
            if high > 0:
                badge_html += f' <span class="severity-high">{high} High</span>'
            if medium > 0:
                badge_html += f' <span class="severity-medium">{medium} Medium</span>'
            if low > 0:
                badge_html += f' <span class="severity-low">{low} Low</span>'
            
            with st.expander(f"{emoji} **{category_name}** ({len(category_scenarios)} scenarios)", expanded=True):
                st.markdown(f"*{description}*")
                if badge_html:
                    st.markdown(badge_html, unsafe_allow_html=True)
                st.markdown("---")
                
                for i, scenario in enumerate(category_scenarios, 1):
                    display_scenario_interactive(scenario, category_name, i)

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
        st.markdown("🤖 **Mode**: AI-Powered (Gemini 2.5 Pro)")
        st.markdown("API Key: ✅ Configured")
    else:
        st.markdown("🎭 **Mode**: Demo Mode")
        st.markdown("API Key: ❌ Not configured")
        st.info("App works in demo mode with sample scenarios. Configure API key for AI-powered generation.")

