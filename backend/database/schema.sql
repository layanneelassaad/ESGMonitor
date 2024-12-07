CREATE TABLE ESG_Scores (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255),
    esg_score FLOAT,
    sentiment_score FLOAT,
    benchmark_score FLOAT,
    violations INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
