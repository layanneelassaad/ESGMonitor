import React, { useState } from "react";
import axios from "axios";

const FileUpload = () => {
    const [file, setFile] = useState(null); // Store the selected file
    const [result, setResult] = useState(null); // Store the result from the backend

    // Handle file selection
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    // Upload the file to the backend
    const handleFileUpload = async () => {
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }

        // Prepare the form data for upload
        const formData = new FormData();
        formData.append("file", file);

        try {
            // Send the file to the backend
            const response = await axios.post(
                "http://127.0.0.1:8000/file-upload/upload-file",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );
            setResult(response.data); // Update the state with the backend response
        } catch (error) {
            console.error("Error uploading file:", error);
            alert("File upload failed. Please try again.");
        }
    };

    return (
        <div style={{ marginBottom: "20px" }}>
            <h2>Upload ESG Document</h2>
            <input type="file" onChange={handleFileChange} />
            <button onClick={handleFileUpload}>Upload</button>
            {result && (
                <div>
                    <h3>ESG Score: {result.esg_score || "N/A"}</h3>
                    <h4>Key Topics</h4>
                    <ul>
                        {result.key_topics && result.key_topics.length > 0 ? (
                            result.key_topics.map((topic, index) => (
                                <li key={index}>{topic}</li>
                            ))
                        ) : (
                            <li>No key topics identified</li>
                        )}
                    </ul>
                    <h4>Recommendations</h4>
                    <ul>
                        {result.recommendations && result.recommendations.length > 0 ? (
                            result.recommendations.map((rec, index) => (
                                <li key={index}>{rec}</li>
                            ))
                        ) : (
                            <li>No recommendations available</li>
                        )}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default FileUpload;
