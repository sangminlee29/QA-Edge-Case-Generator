"""
QA Edge Case Generator - Multi-Page App Landing Page
"""
import streamlit as st

# Page config
st.set_page_config(
    page_title="QA Edge Case Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 1rem;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-header {
    font-size: 1.5rem;
    text-align: center;
    color: #666;
    margin-bottom: 3rem;
}
.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 1.5rem;
    border-left: 4px solid #667eea;
    transition: transform 0.2s;
}
.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}
.feature-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
    color: #333;
}
.feature-desc {
    color: #666;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🤖 QA Edge Case Generator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI 기반 QA 테스트 시나리오 생성 도구</div>', unsafe_allow_html=True)

# Introduction
st.markdown("---")
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 👋 환영합니다!
    
    QA Edge Case Generator는 Google Gemini AI를 활용하여 개발자들이 놓치기 쉬운 
    엣지 케이스를 자동으로 찾아내는 도구입니다.
    
    **주요 기능:**
    - 🎯 AI 기반 테스트 시나리오 자동 생성
    - 📋 Jira 스타일 칸반 보드
    - 🔗 Webhook API 지원
    - ☑️ 인터랙티브 체크리스트
    """)

with col2:
    st.info("""
    **💡 시작하기**
    
    왼쪽 사이드바에서 원하는 
    페이지를 선택하세요!
    """)

st.markdown("---")

# Feature cards
st.markdown("### 📱 사용 가능한 기능")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🎯 QA Generator</div>
        <div class="feature-desc">
            기능 설명을 입력하면 AI가 4가지 카테고리(Functional, Security, 
            Input Validation, Network)로 분류된 테스트 시나리오를 생성합니다.
            <br><br>
            <strong>특징:</strong>
            <ul>
                <li>심각도별 색상 뱃지 (High/Medium/Low)</li>
                <li>접을 수 있는 카테고리</li>
                <li>체크박스로 진행 상황 추적</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📋 Kanban Board</div>
        <div class="feature-desc">
            Jira 스타일의 칸반 보드에서 티켓을 관리하고, 
            "진행 중"으로 이동하면 자동으로 AI가 엣지 케이스를 분석합니다.
            <br><br>
            <strong>특징:</strong>
            <ul>
                <li>Jira 스타일 카드 디자인</li>
                <li>드래그 없이 버튼으로 이동</li>
                <li>자동 AI 분석 트리거</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick start guide
st.markdown("### 🚀 빠른 시작 가이드")

tab1, tab2 = st.tabs(["QA Generator 사용법", "Kanban Board 사용법"])

with tab1:
    st.markdown("""
    1. 왼쪽 사이드바에서 **🎯 QA Generator** 선택
    2. 텍스트 영역에 기능 설명 입력
    3. **시나리오 생성** 버튼 클릭
    4. 생성된 테스트 케이스 확인 및 체크
    """)

with tab2:
    st.markdown("""
    1. 왼쪽 사이드바에서 **📋 Kanban Board** 선택
    2. "할 일" 컬럼의 티켓 확인
    3. **진행 중으로 이동** 버튼 클릭
    4. AI가 자동으로 엣지 케이스 분석
    5. 카드 아래 댓글로 결과 확인
    """)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; color: #999; padding: 2rem;">
    <p>Powered by Google Gemini 2.5 Pro | Made with Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 📖 도움말")
    st.markdown("""
    ### API 설정
    `.streamlit/secrets.toml` 파일에 
    Gemini API 키를 설정하세요.
    
    ### Flask API
    Flask 서버를 실행하면 
    `/webhook` 엔드포인트로 
    프로그래밍 방식 접근이 가능합니다.
    
    ```bash
    python flask_app.py
    ```
    """)
