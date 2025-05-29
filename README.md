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
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

Create a `.env` file in the root directory of the project with the following content:

```env
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH=/full/path/to/your/service-account.json
```

### 5. Set Up Your Google Sheet

- Create a Google Sheet with a tab named `Sheet1`.
- Share it with your Google service account email.

Update the `GOOGLE_SHEET_ID` in your Python code with your actual sheet ID.

### 6. Run the Server

```bash
python sentiment.py
```

You should see the app running on `http://127.0.0.1:5000`.

### 7. Submit a Review (Example)

Use `curl` or Postman:

```bash
curl -X POST http://127.0.0.1:5000/submit-review \
-H "Content-Type: application/json" \
-d '{"name": "Shlok", "Experience": "This product is amazing and exceeded expectations!"}'
```

### 8. Output

- Sentiment is analyzed using OpenAI GPT.
- Name and sentiment are appended to the connected Google Sheet.

---

## ✅ Example Google Sheet Format

| Name  | Sentiment          |
|-------|--------------------|
| Shlok | Extremely positive |

---

## 📌 Notes

- Make sure the Google Sheets API is enabled in your Google Cloud project.
- The service account JSON file must match the one you created in Google Cloud Console.



