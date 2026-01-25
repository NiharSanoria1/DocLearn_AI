from fastapi import FastAPI, HTTPException, UploadFile, File
from uuid import uuid4

# from app.api.routes.upload import router as upload_router
from app.ingestion.pdf_validator import validate_pdf
from app.ingestion.storage import save_pdf
from app.ingestion.quality_checker import check_pdf_quality
from app.ingestion.metadata import create_metadata

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/upload-test")
async def upload_pdf(file: UploadFile = File(...)):
    
    user_id = "test_user"
    pdf_id = str(uuid4())
    
    validate_pdf(file)
    
    pdf_path  = save_pdf(user_id, pdf_id, file)
    
    quality_report = check_pdf_quality(pdf_path)
    
    create_metadata(user_id, pdf_id, pdf_path, quality_report)
    
    return {
        "message": "PDF validated and stored successfully",
        "pdf_id": pdf_id,
        "stored_at": pdf_path,
        "status": quality_report["status"]
    } 
