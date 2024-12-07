from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.file_upload import router as file_upload_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(file_upload_router, prefix="/file-upload")

@app.get("/")
def root():
    return {"message": "Welcome to the ESG Risk Monitor API"}
