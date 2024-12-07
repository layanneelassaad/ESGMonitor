from fastapi import APIRouter
import requests

router = APIRouter()

@router.get("/aggregate-data")
def aggregate_esg_data():
    """
    Aggregates ESG-related data from external sources.
    """
    news_url = "https://newsapi.org/v2/everything?q=ESG&apiKey=YOUR_NEWS_API_KEY"
    try:
        news_response = requests.get(news_url).json()
        return {"news": news_response.get("articles", [])}
    except Exception as e:
        return {"error": str(e)}
