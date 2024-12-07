import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);
    const [sentiment, setSentiment] = useState(null);

    const handleFileChange = (e) => setFile(e.target.files[0]);

    const handleFileUpload = async () => {
        if (!file) {
            alert("Please select a file.");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://127.0.0.1:8000/file-upload/upload-file", formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            setResult(response.data);
        } catch (error) {
            alert("Failed to process the file. Please try again.");
        }
    };

    const handleAnalyzeSentiment = async (text) => {
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/analyze-sentiment",
                { text },
                { headers: { "Content-Type": "application/json" } }
            );
            setSentiment(response.data);
        } catch (error) {
            alert("Failed to analyze sentiment. Please try again.");
        }
    };

    return (
        <div style={{ padding: "20px", maxWidth: "800px", margin: "auto", fontFamily: "Arial" }}>
            <h2>ESG Risk Monitor</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload</button>
            
            {result && (
                <div>
                    <h3>GHG Efforts Summary</h3>
                    <p>{result.ghg_efforts_summary || "No summary available."}</p>

                    <h3>Branch Summaries</h3>
                    <div>
                        {result.branch_summaries &&
                            Object.entries(result.branch_summaries).map(([branch, summary], idx) => (
                                <div key={idx}>
                                    <h4>{branch}</h4>
                                    <p>{summary}</p>
                                </div>
                            ))}
                    </div>

                    <h3>Recommendations</h3>
                    <ul>
                        {result.recommendations &&
                            result.recommendations.map((rec, idx) => <li key={idx}>{rec}</li>)}
                    </ul>
                </div>
            )}

            <div>
                <h3>Sentiment Analysis</h3>
                <textarea rows="4" cols="50" placeholder="Enter text..." onBlur={(e) => handleAnalyzeSentiment(e.target.value)} />
                {sentiment && (
                    <div>
                        <p>Sentiment: {sentiment.sentiment}</p>
                        <p>Confidence: {sentiment.confidence}%</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default FileUpload;
