# QA Edge Case Generator

A dual-server application for generating comprehensive QA test scenarios using Google's Gemini Pro model.

## Features

### Streamlit Web App
- 📝 Simple text area input for feature descriptions
- 🤖 AI-powered test scenario generation using Google Gemini Pro
- 📊 Categorized results across 4 testing dimensions:
  - 🎯 **Functional**: Core functionality and business logic edge cases
  - 🔒 **Security**: Security vulnerabilities and attack vectors
  - ✅ **Input Validation**: Invalid inputs, boundary conditions, data type issues
  - 🌐 **Network**: Network-related issues, timeouts, connectivity problems
- 📂 Interactive UI with expandable categories
- ☑️ Checkboxes to track test completion
- 🎨 Color-coded severity badges (High/Medium/Low)

### Flask API Server
- 🔗 `/webhook` endpoint for programmatic access
- 📋 Generates markdown checklist format
- 🌐 CORS-enabled for cross-origin requests
- ❤️ Health check endpoint

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Gemini API Key

1. Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create/Edit `.streamlit/secrets.toml` and add your API key:

```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

### 3. Run the Applications

#### Option A: Streamlit App Only

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

#### Option B: Flask API Server Only

```bash
python flask_app.py
```

The server will start at `http://localhost:5000`

#### Option C: Both Servers Simultaneously

Terminal 1 (Streamlit):
```bash
streamlit run app.py
```

Terminal 2 (Flask):
```bash
python flask_app.py
```

## Usage

### Streamlit Web App

1. Open `http://localhost:8501` in your browser
2. Enter a detailed description of your feature in the text area
3. Click the "🚀 시나리오 생성 (Generate Scenarios)" button
4. Review the generated test scenarios organized by category
5. Check off completed tests using the checkboxes

### Flask API Server

#### Endpoint: POST /webhook

Generate QA edge case checklist in markdown format.

**Request:**
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "User Login Feature",
    "description": "A login form that accepts email and password, with a Remember Me checkbox and Forgot Password link."
  }'
```

**Response:**
```json
{
  "result": "## 🎯 Functional (기능)\n- [ ] 유효한 이메일과 비밀번호로 로그인 성공 테스트\n- [ ] 잘못된 비밀번호 입력 시 에러 메시지 표시 확인\n..."
}
```

#### Endpoint: GET /health

Health check endpoint.

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "gemini_api_configured": true
}
```

## Requirements

- Python 3.9+
- Streamlit 1.28.0+
- Flask 3.0.0+
- Google Generative AI SDK (google-generativeai)
- Valid Gemini API key

## Project Structure

```
.
├── app.py              # Streamlit web application
├── flask_app.py        # Flask API server
├── config.py           # Shared configuration (API key loader)
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── secrets.toml   # API key configuration
└── README.md          # This file
```

## Notes

- The application uses Gemini Pro for generating test scenarios.
- API calls are subject to Google Gemini API pricing and rate limits.
- Keep your API key secure and never commit it to version control.
- Both servers can run simultaneously on different ports (8501 for Streamlit, 5000 for Flask).

## Troubleshooting

**API Key Error**: If you see an error about the API key, make sure:
- The `.streamlit/secrets.toml` file exists
- Your API key is correctly configured with the key `GEMINI_API_KEY`
- The API key is valid

**Connection Error**: Check your internet connection.

**Port Already in Use**: 
- For Streamlit: Use `streamlit run app.py --server.port 8502`
- For Flask: Modify the port in `flask_app.py` or set `FLASK_RUN_PORT` environment variable