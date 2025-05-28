from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Enable CORS (so frontend can call the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Hugging Face sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# Define request body format
class TextInput(BaseModel):
    text: str

# Define the sentiment analysis route
@app.post("/analyze")
async def analyze_sentiment(input: TextInput):
    result = sentiment_pipeline(input.text)[0]
    return {
        "label": result["label"],
        "score": round(result["score"], 4)
    }

# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Sentiment Analysis API is running"}
