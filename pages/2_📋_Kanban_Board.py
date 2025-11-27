"""
Jira-Style Kanban Board
AI-powered QA edge case analysis when tickets move to "In Progress"
"""
import streamlit as st
from config import get_ai_model, get_generation_config
import textwrap
import json

# Page config
st.set_page_config(
    page_title="Kanban Board - QA Generator",
    page_icon="📋",
    layout="wide"
)

# Initialize AI Model (supports both Gemini API Key and Vertex AI)
@st.cache_resource
def get_ai_model_cached():
    return get_ai_model()

model = get_ai_model_cached()

# Jira-style CSS
st.markdown("""
<style>
/* Kanban board layout */
.kanban-column {
    background-color: #f4f5f7;
    border-radius: 8px;
    padding: 1rem;
    min-height: 500px;
}

/* Jira-style card */
.jira-card {
    background: white;
    border-radius: 4px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    border-left: 4px solid;
    transition: all 0.2s ease;
}

.jira-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    transform: translateY(-2px);
}

.jira-card.todo {
    border-left-color: #0052CC;
}

.jira-card.in-progress {
    border-left-color: #FFAB00;
}

.jira-card.done {
    border-left-color: #36B37E;
}

.card-id {
    font-size: 0.75rem;
    color: #5E6C84;
    font-weight: 600;
    margin-bottom: 0.25rem;
}

.card-summary {
    font-size: 1rem;
    font-weight: 600;
    color: #172B4D;
    margin-bottom: 0.5rem;
}

.card-description {
    font-size: 0.875rem;
    color: #5E6C84;
    line-height: 1.4;
    margin-bottom: 0.75rem;
}

.column-header {
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    color: #5E6C84;
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-count {
    background: #DFE1E6;
    border-radius: 12px;
    padding: 2px 8px;
    font-size: 0.75rem;
}

/* Edge case comments */
.edge-case-comment {
    background: #F4F5F7;
    border-left: 3px solid #0052CC;
    padding: 0.75rem;
    margin-top: 0.75rem;
    border-radius: 4px;
    font-size: 0.875rem;
}

.comment-header {
    font-weight: 600;
    color: #172B4D;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.ai-badge {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cards' not in st.session_state:
    st.session_state.cards = [
        {
            "id": "PROJ-101",
            "summary": "사용자 로그인 기능",
            "description": "이메일과 비밀번호로 로그인하고, 로그인 상태 유지 옵션 제공",
            "status": "To Do",
            "edge_cases": None
        },
        {
            "id": "PROJ-102",
            "summary": "결제 시스템 통합",
            "description": "신용카드 및 간편결제 지원, 결제 실패 시 재시도 로직 구현",
            "status": "To Do",
            "edge_cases": None
        },
        {
            "id": "PROJ-103",
            "summary": "파일 업로드 기능",
            "description": "이미지, 문서 파일 업로드 지원, 최대 10MB 제한",
            "status": "To Do",
            "edge_cases": None
        }
    ]

# Function to analyze ticket with AI
def analyze_ticket(card):
    """Generate edge cases using Gemini API"""
    if not model:
        return "⚠️ Gemini API 키가 설정되지 않았습니다."
    
    prompt = f"""너는 구글 출신의 20년 차 시니어 QA 엔지니어다. 
개발자들이 흔히 놓치는 사소하지만 치명적인 엣지 케이스(Edge Case)를 찾아내는 것이 목표다.

티켓 정보:
- ID: {card['id']}
- 요약: {card['summary']}
- 설명: {card['description']}

위 티켓에 대한 QA 엣지 케이스를 JSON 형식으로 작성하라.
4가지 카테고리(Functional, Security, Input Validation, Network)로 나누고,
각 카테고리당 3-5개의 구체적인 테스트 케이스를 작성하라.

각 테스트 케이스에는 다음 중요도 중 하나를 할당하라:
- CRITICAL: 시스템 장애나 보안 위협
- HIGH: 심각한 사용자 경험 저하
- MEDIUM: 개선 필요

응답 형식 (JSON):
{{
    "edge_cases": [
        {{
            "category": "Functional",
            "emoji": "🎯",
            "cases": [
                {{ "description": "테스트 케이스 내용", "priority": "CRITICAL" }},
                {{ "description": "테스트 케이스 내용", "priority": "HIGH" }}
            ]
        }},
        {{
            "category": "Security",
            "emoji": "🔒",
            "cases": [...]
        }}
    ]
}}
"""

    try:
        # Configure for JSON response
        generation_config = get_generation_config(response_mime_type="application/json")
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text.strip()
    except Exception as e:
        return json.dumps({"error": str(e)})

# Function to generate next ticket ID
def generate_ticket_id():
    """Generate next ticket ID based on existing tickets"""
    existing_ids = [card['id'] for card in st.session_state.cards]
    
    # Extract numbers from existing IDs (e.g., "PROJ-101" -> 101)
    numbers = []
    for ticket_id in existing_ids:
        try:
            # Try to extract number from format like "PROJ-101"
            if '-' in ticket_id:
                num = int(ticket_id.split('-')[-1])
                numbers.append(num)
        except ValueError:
            continue
    
    # Generate next number
    if numbers:
        next_num = max(numbers) + 1
    else:
        next_num = 101  # Start from 101 if no existing tickets
    
    return f"PROJ-{next_num}"

# Function to add new card
def add_card(summary, description):
    """Add a new card to the To Do list with auto-generated ID"""
    ticket_id = generate_ticket_id()
    
    new_card = {
        "id": ticket_id,
        "summary": summary,
        "description": description,
        "status": "To Do",
        "edge_cases": None
    }
    # Insert at the beginning of the list to show at the top
    st.session_state.cards.insert(0, new_card)
    return True, f"티켓 '{ticket_id}'가 추가되었습니다."

# Function to move card
def move_card(card_id, new_status):
    """Move card to new status and trigger AI analysis if moving to In Progress"""
    for card in st.session_state.cards:
        if card['id'] == card_id:
            old_status = card['status']
            card['status'] = new_status
            
            # Trigger AI analysis when moving to In Progress
            if new_status == "In Progress" and card['edge_cases'] is None:
                with st.spinner(f"🤖 AI QA Bot이 {card_id} 티켓을 분석 중입니다..."):
                    card['edge_cases'] = analyze_ticket(card)
                st.success(f"✅ {card_id} 분석 완료!")
            
            break

# Header
st.title("📋 Kanban Board")
st.markdown("*Jira 스타일 칸반 보드 - 티켓을 '진행 중'으로 이동하면 AI가 자동으로 엣지 케이스를 분석합니다*")

# Add new ticket form
with st.expander("➕ 새 티켓 추가", expanded=False):
    with st.form("add_ticket_form", clear_on_submit=True):
        ticket_summary = st.text_input("요약", placeholder="예: 사용자 프로필 수정 기능", help="티켓의 간단한 요약을 입력하세요")
        
        ticket_description = st.text_area("설명", placeholder="상세한 설명을 입력하세요...", height=100, help="티켓의 상세한 설명을 입력하세요")
        
        col_btn1, col_btn2 = st.columns([1, 5])
        with col_btn1:
            submitted = st.form_submit_button("추가", type="primary", use_container_width=True)
        
        if submitted:
            if not ticket_summary.strip():
                st.error("요약을 입력하세요.")
            elif not ticket_description.strip():
                st.error("설명을 입력하세요.")
            else:
                success, message = add_card(ticket_summary.strip(), ticket_description.strip())
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

st.markdown("---")

# Kanban columns
col_todo, col_progress, col_done = st.columns(3)

# Helper function to render card
def render_card(card):
    """Render a Jira-style card"""
    status_class = card['status'].lower().replace(" ", "-")
    
    card_html = f"""
    <div class="jira-card {status_class}">
        <div class="card-id">{card['id']}</div>
        <div class="card-summary">{card['summary']}</div>
        <div class="card-description">{card['description']}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    
    # Action buttons
    if card['status'] == "To Do":
        if st.button(f"▶️ 진행 중으로 이동", key=f"move_{card['id']}", use_container_width=True):
            move_card(card['id'], "In Progress")
            st.rerun()
    elif card['status'] == "In Progress":
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"◀️ 할 일로", key=f"back_{card['id']}", use_container_width=True):
                move_card(card['id'], "To Do")
                st.rerun()
        with col2:
            if st.button(f"✅ 완료", key=f"done_{card['id']}", use_container_width=True):
                move_card(card['id'], "Done")
                st.rerun()
    elif card['status'] == "Done":
        if st.button(f"↩️ 진행 중으로", key=f"reopen_{card['id']}", use_container_width=True):
            move_card(card['id'], "In Progress")
            st.rerun()
    
    
    # Show edge cases if available
    if card['edge_cases']:
        # Parse and display edge cases
        try:
            # Try parsing as JSON first
            import json
            data = json.loads(card['edge_cases'])
            
            if isinstance(data, dict) and "error" in data:
                st.error(f"AI 분석 중 오류가 발생했습니다: {data['error']}")
            
            elif isinstance(data, dict) and "edge_cases" in data:
                # Create expander for AI analysis results inside the card
                with st.expander("🤖 **AI QA Bot 분석 결과**", expanded=False):
                    # Iterate through categories
                    for category_data in data['edge_cases']:
                        emoji = category_data.get('emoji', '📋')
                        category = category_data.get('category', 'General')
                        cases = category_data.get('cases', [])
                        
                        # Sort cases by priority: CRITICAL -> HIGH -> MEDIUM
                        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2}
                        cases = sorted(cases, key=lambda x: priority_order.get(x.get('priority', 'MEDIUM'), 2))
                        
                        # Color mapping for categories
                        colors = {
                            'Functional': {'bg': '#EBF4FF', 'border': '#3182CE', 'text': '#2C5282'},
                            'Security': {'bg': '#FFF5F5', 'border': '#E53E3E', 'text': '#742A2A'},
                            'Input Validation': {'bg': '#F0FFF4', 'border': '#38A169', 'text': '#22543D'},
                            'Network': {'bg': '#FFFAF0', 'border': '#DD6B20', 'text': '#7C2D12'}
                        }
                        
                        # Match by category name or emoji if needed
                        color_scheme = colors.get(category, {'bg': '#F7FAFC', 'border': '#718096', 'text': '#2D3748'})
                        
                        # Create expander for each category
                        with st.expander(f"{emoji} **{category}**", expanded=True):
                            for i, case in enumerate(cases):
                                test_case = case.get('description', '')
                                priority = case.get('priority', 'MEDIUM')
                                
                                # Priority colors
                                priority_colors = {
                                    'CRITICAL': {'bg': '#DC2626', 'text': 'white', 'icon': '🔥'},
                                    'HIGH': {'bg': '#F59E0B', 'text': 'white', 'icon': '⚠️'},
                                    'MEDIUM': {'bg': '#10B981', 'text': 'white', 'icon': '📌'}
                                }
                                
                                p_color = priority_colors.get(priority, priority_colors['MEDIUM'])
                                
                                # Border style
                                border_style = f"1px solid {color_scheme['border']}40"
                                if priority == 'CRITICAL':
                                    border_style = f"2px solid {priority_colors['CRITICAL']['bg']}"
                                elif priority == 'HIGH':
                                    border_style = f"2px solid {priority_colors['HIGH']['bg']}"
                                
                                # Layout: Checkbox on left, content on right
                                col_check, col_content = st.columns([0.05, 0.95])
                                
                                with col_check:
                                    # Unique key for checkbox
                                    check_key = f"check_{card['id']}_{category}_{i}"
                                    is_checked = st.checkbox(
                                        "",
                                        key=check_key,
                                        label_visibility="collapsed"
                                    )
                                
                                with col_content:
                                    # Apply strikethrough if checked
                                    text_style = "text-decoration: line-through; opacity: 0.6;" if is_checked else ""
                                    
                                    # Get badge values
                                    bg_color = p_color['bg']
                                    text_color = p_color['text']
                                    icon = p_color['icon']
                                    
                                    # Content card with proper styling - build badge inline to avoid parsing issues
                                    box_shadow = 'box-shadow: 0 2px 8px rgba(220, 38, 38, 0.2);' if priority == 'CRITICAL' else ''
                                    
                                    item_html = f"""
<style>
@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.7; }}
}}
</style>
<div style="padding: 0.75rem; margin-bottom: 0.75rem; background: white; border-radius: 6px; border: {border_style}; transition: all 0.2s ease; {box_shadow}">
    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
        <div style="background: {bg_color}; color: {text_color}; padding: 4px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; display: inline-flex; align-items: center; gap: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
            <span>{icon}</span>
            <span>{priority}</span>
        </div>
    </div>
    <div style="color: {color_scheme['text']}; font-size: 0.95rem; line-height: 1.6; {text_style}">{test_case}</div>
</div>
"""
                                    st.markdown(item_html, unsafe_allow_html=True)

        except json.JSONDecodeError:
            # Fallback for legacy markdown data
            st.warning("⚠️ 이전 형식의 데이터입니다. (Markdown)")
            st.markdown(card['edge_cases'])
        except Exception as e:
            st.error(f"데이터 렌더링 오류: {str(e)}")
            st.code(card['edge_cases'])
    
    
    st.markdown("<br>", unsafe_allow_html=True)

# Render columns
with col_todo:
    todo_cards = [c for c in st.session_state.cards if c['status'] == "To Do"]
    st.markdown(f"""
    <div class="column-header">
        <span>할 일 (TO DO)</span>
        <span class="card-count">{len(todo_cards)}</span>
    </div>
    """, unsafe_allow_html=True)
    
    for card in todo_cards:
        render_card(card)

with col_progress:
    progress_cards = [c for c in st.session_state.cards if c['status'] == "In Progress"]
    st.markdown(f"""
    <div class="column-header">
        <span>진행 중 (IN PROGRESS)</span>
        <span class="card-count">{len(progress_cards)}</span>
    </div>
    """, unsafe_allow_html=True)
    
    for card in progress_cards:
        render_card(card)

with col_done:
    done_cards = [c for c in st.session_state.cards if c['status'] == "Done"]
    st.markdown(f"""
    <div class="column-header">
        <span>완료 (DONE)</span>
        <span class="card-count">{len(done_cards)}</span>
    </div>
    """, unsafe_allow_html=True)
    
    for card in done_cards:
        render_card(card)

# Sidebar
with st.sidebar:
    st.markdown("## 📖 사용 방법")
    st.markdown("""
    1. **할 일** 컬럼의 티켓 확인
    2. **진행 중으로 이동** 버튼 클릭
    3. AI가 자동으로 엣지 케이스 분석
    4. 카드 아래 AI 댓글로 결과 확인
    5. 작업 완료 후 **완료** 버튼 클릭
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ 설정")
    if model:
        st.success("🤖 AI Bot: 활성화")
    else:
        st.error("🤖 AI Bot: 비활성화")
        st.info("Gemini API 키를 설정하세요")
