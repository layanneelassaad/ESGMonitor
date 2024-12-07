import React, { useState } from "react";
import axios from "axios";

const RiskPrediction = () => {
    const [historicalData, setHistoricalData] = useState({ time: [], esg_scores: [] });
    const [futureTime, setFutureTime] = useState("");
    const [predictedScore, setPredictedScore] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const fetchPrediction = async () => {
        if (!futureTime || historicalData.time.length === 0 || historicalData.esg_scores.length === 0) {
            alert("Please provide valid historical data and future time.");
            return;
        }

        setIsLoading(true);
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/predictive-modeling/predict-risk",
                { historical_data: historicalData, future_time: parseInt(futureTime) }
            );
            setPredictedScore(response.data.predicted_esg_score);
        } catch (error) {
            console.error("Error predicting ESG risk:", error);
            alert("Prediction failed. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div>
            <h2>Risk Prediction</h2>
            <div>
                <label>Historical Time (comma-separated): </label>
                <input
                    type="text"
                    onChange={(e) =>
                        setHistoricalData({
                            ...historicalData,
                            time: e.target.value.split(",").map((v) => parseInt(v)),
                        })
                    }
                />
            </div>
            <div>
                <label>Historical ESG Scores (comma-separated): </label>
                <input
                    type="text"
                    onChange={(e) =>
                        setHistoricalData({
                            ...historicalData,
                            esg_scores: e.target.value.split(",").map((v) => parseFloat(v)),
                        })
                    }
                />
            </div>
            <div>
                <label>Future Time: </label>
                <input
                    type="number"
                    value={futureTime}
                    onChange={(e) => setFutureTime(e.target.value)}
                />
            </div>
            <button onClick={fetchPrediction} disabled={isLoading}>
                {isLoading ? "Predicting..." : "Predict"}
            </button>
            {predictedScore !== null && (
                <p>
                    Predicted ESG Score for Future Time: <strong>{predictedScore.toFixed(2)}</strong>
                </p>
            )}
        </div>
    );
};

export default RiskPrediction;
