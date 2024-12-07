from transformers import pipeline
from fastapi import APIRouter, HTTPException

sentiment_pipeline = pipeline("sentiment-analysis")
router = APIRouter()

@router.post("/analyze-sentiment")
def analyze_sentiment(text: str):
    """
    Analyze sentiment of input text.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text is empty or invalid.")
    try:
        # Limit input to 512 characters
        trimmed_text = text[:512]
        result = sentiment_pipeline(trimmed_text)[0]
        return {
            "sentiment": result["label"],
            "confidence": round(result["score"] * 100, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing sentiment: {e}")
