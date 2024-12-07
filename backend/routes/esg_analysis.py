from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from models.metrics_extraction import process_esg_report
import os

router = APIRouter()

@router.post("/analyze-esg")
async def analyze_esg(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Analyze ESG report
        results = process_esg_report(file_path)

        # Clean up the temporary file
        os.remove(file_path)

        return JSONResponse(content=results)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
