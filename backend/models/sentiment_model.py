from transformers import pipeline

# Load the sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=0)

def analyze_sentiment(text):
    """
    Analyzes the sentiment of the provided text.
    """
    return sentiment_analyzer(text)
