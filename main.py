from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Enable CORS so the frontend can call the backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Sentimental Analysis Bot is live!"}

@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon"}

# Serve the frontend HTML
@app.get("/app", response_class=HTMLResponse)
def serve_frontend():
    with open("frontend.html", "r", encoding="utf-8") as f:
        return f.read()

# HuggingFace API setup
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
API_TOKEN = os.getenv("HF_TOKEN")  # Make sure this is set on Render

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(input: TextInput):
    payload = {"inputs": input.text}
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    if isinstance(result, dict) and result.get("error"):
        return {"error": result["error"]}

    prediction = result[0][0]
    return {
        "label": prediction["label"],
        "score": round(prediction["score"], 4)
    }
