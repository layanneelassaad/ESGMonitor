from fastapi import APIRouter
from models.predictive_model import train_model, predict_future_score

router = APIRouter()

@router.post("/predict-risk")
def predict_future_risk(historical_data: dict, future_time: int):
    """
    Predicts future ESG risk scores based on historical data.
    """
    # Train the model using historical data
    model = train_model(historical_data)
    # Predict future ESG score
    predicted_score = predict_future_score(model, future_time)
    return {"predicted_esg_score": round(predicted_score[0], 2)}
