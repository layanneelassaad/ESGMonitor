import React, { useState } from "react";
import axios from "axios";

const DocumentAnalysis = () => {
    const [text, setText] = useState("");
    const [analysis, setAnalysis] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const analyzeDocument = () => {
        if (!text.trim()) {
            alert("Please enter document text.");
            return;
        }

        setIsLoading(true);
        axios
            .post("http://127.0.0.1:8000/nlp-analysis/analyze-document", { text })
            .then((response) => setAnalysis(response.data))
            .catch((error) => console.error("Error analyzing document:", error))
            .finally(() => setIsLoading(false));
    };

    return (
        <div style={{ marginBottom: "20px" }}>
            <h2>Document Analysis</h2>
            <textarea
                rows="5"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste ESG-related document text here"
                style={{ width: "100%" }}
            />
            <br />
            <button onClick={analyzeDocument} disabled={isLoading}>
                {isLoading ? "Analyzing..." : "Analyze"}
            </button>
            {analysis && (
                <div>
                    <h3>Key Topics</h3>
                    <ul>
                        {analysis.key_topics?.map((topic, index) => (
                            <li key={index}>{topic}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default DocumentAnalysis;
