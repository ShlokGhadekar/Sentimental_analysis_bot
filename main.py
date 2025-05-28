from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Sentimental Analysis Bot is live!"}
    
@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon"}
    
API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
API_TOKEN = os.getenv("HF_TOKEN")  # store this securely

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
