# QA Edge Case Generator

A Streamlit-based web application that generates comprehensive QA test scenarios using OpenAI's GPT-4 model.

## Features

- 📝 Simple text area input for feature descriptions
- 🤖 AI-powered test scenario generation using OpenAI GPT-4
- 📊 Categorized results across 4 testing dimensions:
  - 🎯 **Functional**: Core functionality and business logic edge cases
  - 🔒 **Security**: Security vulnerabilities and attack vectors
  - ✅ **Input Validation**: Invalid inputs, boundary conditions, data type issues
  - 🌐 **Network**: Network-related issues, timeouts, connectivity problems

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API Key

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Edit `.streamlit/secrets.toml` and replace `your-api-key-here` with your actual API key:

```toml
OPENAI_API_KEY = "sk-your-actual-api-key"
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

1. Enter a detailed description of your feature in the text area
2. Click the "🚀 시나리오 생성 (Generate Scenarios)" button
3. Review the generated test scenarios organized by category

### Example Feature Description

```
A login form that accepts email and password, with a 'Remember Me' checkbox 
and 'Forgot Password' link. Users can sign in with their credentials and 
optionally stay logged in for 30 days.
```

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- OpenAI Python SDK 1.3.0+
- Valid OpenAI API key

## Notes

- The application uses GPT-4 for generating test scenarios
- API calls may incur costs based on your OpenAI usage plan
- Keep your API key secure and never commit it to version control

## Troubleshooting

**API Key Error**: If you see an error about the API key, make sure:
- The `.streamlit/secrets.toml` file exists
- Your API key is correctly formatted (starts with `sk-`)
- The API key is valid and has sufficient credits

**Connection Error**: Check your internet connection and OpenAI API status at [status.openai.com](https://status.openai.com)
