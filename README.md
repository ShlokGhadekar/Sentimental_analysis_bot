# 🧠 Sentiment Analysis API

A Flask-based API that takes a user review, analyzes its sentiment using OpenAI GPT, and logs the name and sentiment to a Google Sheet.

---

## 🔧 Requirements

- Python 3.7+
- OpenAI API key
- Google Cloud service account with Sheets API enabled
- A Google Sheet shared with the service account

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/sentiment-analysis.git
cd sentiment-analysis

Create a virtual Environment

python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

install dependencies

pip install -r requirements.txt

create a .env file

OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH=/full/path/to/your/service-account.json

