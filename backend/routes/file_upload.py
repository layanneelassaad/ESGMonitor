import os
import chardet
import pdfplumber
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from models.metrics_extraction import summarize_by_branches, generate_esg_recommendations, summarize_ghg_efforts
from models.goal_achievement_extraction import extract_goals_and_achievements




router = APIRouter()

def extract_text_from_file(file_path, file_type):
    try:
        print(f"Extracting text from file: {file_path}, file type: {file_type}")
        if file_type == "pdf":
            with pdfplumber.open(file_path) as pdf:
                text = "".join(page.extract_text() or "" for page in pdf.pages)
        else:
            with open(file_path, "rb") as file:
                detected_encoding = chardet.detect(file.read()).get("encoding", "utf-8")
                file.seek(0)
                text = file.read().decode(detected_encoding, errors="replace")
        if not text.strip():
            raise ValueError("The file is empty or unreadable.")
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        raise


@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    try:
        print(f"Received file: {file.filename}")
        file_type = "pdf" if file.filename.endswith(".pdf") else "text"
        file_path = f"/tmp/{file.filename}"

        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        print(f"Saved file to temporary path: {file_path}")

        # Extract text from file
        text = extract_text_from_file(file_path, file_type)
        print("Text extraction complete. Starting analysis...")

        # Summarize GHG efforts
        ghg_summary = summarize_ghg_efforts(text)
        print(f"GHG Summary: {ghg_summary}")

        # Generate recommendations (optional)
        branch_summaries = summarize_by_branches(text)
        recommendations = generate_esg_recommendations({}, branch_summaries)
        print(f"Generated Recommendations: {recommendations}")

        # Clean up the temporary file
        os.remove(file_path)
        print(f"Temporary file deleted: {file_path}")

        # Return analysis results
        return JSONResponse(content={
            "ghg_efforts_summary": ghg_summary,
            "recommendations": recommendations,
        })
    except Exception as e:
        print(f"Error in file upload and processing: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)