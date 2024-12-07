import numpy as np
from sklearn.linear_model import LinearRegression

def train_model(historical_data):
    """
    Trains a predictive model for ESG scores.
    """
    X = np.array(historical_data["time"]).reshape(-1, 1)
    y = np.array(historical_data["esg_scores"])
    model = LinearRegression()
    model.fit(X, y)
    return model

def predict_future_score(model, future_time):
    """
    Predicts the ESG score for a future time.
    """
    return model.predict(np.array([future_time]).reshape(-1, 1))
