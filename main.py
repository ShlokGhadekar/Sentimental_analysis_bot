from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Enable CORS (allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis Bot is live!"}

@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon available."}

# Serve the static frontend HTML page
@app.get("/app", response_class=HTMLResponse)
def serve_frontend():
    try:
        with open("frontend.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Frontend not found.")

# HuggingFace API details
HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HF_API_TOKEN = os.getenv("HF_TOKEN")

if not HF_API_TOKEN:
    raise RuntimeError("HuggingFace API token (HF_TOKEN) not set in environment variables.")

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(input: TextInput):
    payload = {"inputs": input.text}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"API request failed: {str(e)}")

    if isinstance(result, dict) and result.get("error"):
        raise HTTPException(status_code=400, detail=result["error"])

    prediction = result[0][0]
    return {
        "label": prediction["label"],
        "score": round(prediction["score"], 4)
    }
