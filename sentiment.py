import os
from flask import Flask, request, jsonify
from openai import OpenAI
import gspread
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH = os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH")
if not GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH:
    raise ValueError("GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH environment variable not set.")

GOOGLE_SHEET_ID = "1Bt-3Pje2mhs71t2HKy1yq0RqpBYH2CVMJ5aBf6G5Quo"  # Your Sheet ID
GOOGLE_SHEET_NAME = "Sheet1"  # Your sheet tab name

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Google Sheets client
try:
    gc = gspread.service_account(filename=GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH)
    spreadsheet = gc.open_by_key(GOOGLE_SHEET_ID)
    worksheet = spreadsheet.worksheet(GOOGLE_SHEET_NAME)
except Exception as e:
    print(f"Error initializing Google Sheets: {e}")
    worksheet = None

@app.route('/', methods=['GET'])
def home():
    # Simple HTML form for browser input
    return '''
    <h2>Submit your review</h2>
    <form action="/submit-review" method="post">
      Name: <input type="text" name="name" required><br><br>
      Experience:<br>
      <textarea name="Experience" rows="4" cols="50" required></textarea><br><br>
      <input type="submit" value="Submit Review">
    </form>
    '''

@app.route('/submit-review', methods=['POST'])
def submit_review():
    # Accept JSON or form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    user_name = data.get("name")
    user_experience = data.get("Experience")

    if not user_name or not user_experience:
        return jsonify({"error": "Missing 'name' or 'Experience' in payload"}), 400

    print(f"Received review from {user_name}: {user_experience}")

    # Perform sentiment analysis
    sentiment = analyze_sentiment(user_experience)
    print(f"Sentiment analysis result: {sentiment}")

    # Save to Google Sheets
    if worksheet:
        try:
            row_to_append = [user_name, sentiment]
            worksheet.append_row(row_to_append)
            print(f"Appended to Google Sheets: Name='{user_name}', Sentiment='{sentiment}'")
        except Exception as e:
            print(f"Error appending to Google Sheets: {e}")
            return jsonify({
                "status": "Review processed, but failed to save to Google Sheets",
                "sentiment": sentiment
            }), 500
    else:
        print("Google Sheets not initialized. Skipping save operation.")
        return jsonify({
            "status": "Review processed, but Google Sheets not configured",
            "sentiment": sentiment
        }), 200

    return jsonify({
        "status": "Review processed and saved successfully",
        "sentiment": sentiment
    }), 200

def analyze_sentiment(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in sentiment analysis. Determine if the review is:\n\n"
                               "Extremely positive\npositive\nneutral\nnegative\nExtremely negative\n\n"
                               "Respond with only one of these 5 options."
                },
                {"role": "user", "content": text}
            ],
            max_tokens=20
        )
        sentiment = response.choices[0].message.content.strip()
        valid_sentiments = ["Extremely positive", "positive", "neutral", "negative", "Extremely negative"]
        return sentiment if sentiment in valid_sentiments else "Invalid sentiment"
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error analyzing sentiment"

if __name__ == '__main__':
    """
    To run:
    1. Create a `.env` file with:
        OPENAI_API_KEY=your_openai_key
        GOOGLE_SHEETS_SERVICE_ACCOUNT_PATH=path_to_service_account.json

    2. Save the service account JSON from Google Cloud Console.

    3. Run:
        python sentiment.py

    4. Open browser at http://127.0.0.1:5000/ to submit a review via form

    5. Or test with curl:
        curl -X POST http://127.0.0.1:5000/submit-review \
        -H "Content-Type: application/json" \
        -d '{"name": "Shlok", "Experience": "This product is amazing and exceeded expectations!"}'
    """
    app.run(debug=True)