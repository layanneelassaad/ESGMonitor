import React, { useState } from "react";
import axios from "axios";

const SentimentAnalysis = () => {
    const [text, setText] = useState("");
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleAnalyzeSentiment = async () => {
        if (!text.trim()) {
            alert("Please enter some text.");
            return;
        }

        setIsLoading(true);
        try {
            const response = await axios.post("http://127.0.0.1:8000/sentiment-analysis/analyze", { text });
            setResult(response.data);
        } catch (error) {
            alert("Failed to analyze sentiment. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div style={{ marginTop: "20px", fontFamily: "Arial, sans-serif" }}>
            <h2>Sentiment Analysis</h2>
            <textarea
                rows="4"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter text to analyze sentiment"
                style={{ width: "100%", marginBottom: "10px", padding: "10px", borderRadius: "5px", border: "1px solid #ccc" }}
            />
            <button onClick={handleAnalyzeSentiment} disabled={isLoading}>
                {isLoading ? "Analyzing..." : "Analyze Sentiment"}
            </button>
            {result && (
                <div style={{ marginTop: "20px", padding: "10px", border: "1px solid #ccc", borderRadius: "8px" }}>
                    <h3>Sentiment Analysis Result</h3>
                    <p><strong>Sentiment:</strong> {result.sentiment}</p>
                    <p><strong>Score:</strong> {result.score}%</p>
                </div>
            )}
        </div>
    );
};

export default SentimentAnalysis;
