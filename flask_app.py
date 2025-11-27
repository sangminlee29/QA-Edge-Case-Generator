"""
Flask Web Server for QA Edge Case Generator
Provides webhook endpoint for generating QA test case checklists.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import get_ai_model, get_generation_config

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize AI Model (supports both Gemini API Key and Vertex AI)
model = get_ai_model()
if not model:
    print("Warning: AI API not configured. Server will return errors for webhook requests.")

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint for generating QA edge case checklists.
    
    Request JSON:
        {
            "summary": "Feature title",
            "description": "Feature description"
        }
    
    Response JSON:
        {
            "result": "Markdown checklist text"
        }
    """
    # Validate request
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    # Validate required fields
    summary = data.get('summary')
    description = data.get('description')
    
    if not summary:
        return jsonify({"error": "Missing required field: summary"}), 400
    
    if not description:
        return jsonify({"error": "Missing required field: description"}), 400
    
    # Check if AI model is available
    if not model:
        return jsonify({"error": "AI API not configured"}), 500
    
    try:
        # Create prompt for Gemini
        prompt = f"""너는 구글 출신의 20년 차 시니어 QA 엔지니어다. 개발자들이 흔히 놓치는 사소하지만 치명적인 엣지 케이스(Edge Case)를 찾아내는 것이 목표다.

당신의 전문성:
- 20년간 수천 개의 프로덕션 버그를 분석한 경험
- 사용자들이 예상치 못한 방식으로 시스템을 사용하는 패턴 파악
- 경계 조건, 동시성 문제, 보안 취약점을 찾아내는 능력
- 단순한 테스트가 아닌, 실제로 프로덕션에서 발생할 수 있는 치명적인 시나리오 발굴

Feature Summary:
{summary}

Feature Description:
{description}

위 기능에 대한 QA 엣지 케이스 테스트 체크리스트를 마크다운 형식으로 작성하라.

다음 4가지 카테고리로 구성:
1. **Functional (기능)** - 핵심 기능과 비즈니스 로직의 엣지 케이스
2. **Security (보안)** - 보안 취약점과 공격 벡터
3. **Input Validation (입력 검증)** - 잘못된 입력, 경계 조건, 데이터 타입 이슈
4. **Network (네트워크)** - 네트워크 관련 문제, 타임아웃, 연결 문제

각 카테고리별로 5-7개의 구체적인 테스트 케이스를 작성하고, 마크다운 체크박스 형식(- [ ])으로 출력하라.

출력 형식 예시:
## 🎯 Functional (기능)
- [ ] 테스트 케이스 1
- [ ] 테스트 케이스 2

## 🔒 Security (보안)
- [ ] 테스트 케이스 1
- [ ] 테스트 케이스 2

마크다운 텍스트만 반환하라. 추가 설명 없이."""

        # Call AI API
        generation_config = get_generation_config(temperature=0.7)
        response = model.generate_content(prompt, generation_config=generation_config)
        result_text = response.text.strip()
        
        # Return result
        return jsonify({"result": result_text}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate checklist: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "ai_api_configured": model is not None
    }), 200

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    print(f"📡 AI API: {'✅ Configured' if model else '❌ Not configured'}")
    print("🔗 Endpoints:")
    print("   - POST /webhook - Generate QA checklist")
    print("   - GET  /health  - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)
