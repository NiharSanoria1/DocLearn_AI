from fastapi import HTTPException , UploadFile, APIRouter, File
from uuid import uuid4

from app.ingestion.pdf_validator import validate_pdf
from app.ingestion.storage import save_pdf
from app.ingestion.quality_checker import check_pdf_quality
from app.ingestion.metadata import create_metadata 


router = APIRouter()

@router.post('/upload')
async def upload_pdf(file: UploadFile = File(...)):
    
    pdf_id = str(uuid4())
    user_id = "demo user"
    
    # basic validation
    validate_pdf(file)
    
    # save pdf
    pdf_path = save_pdf(user_id, pdf_id, file)
    
    # quality check
    quality_info = quality_info(pdf_path)
    
    # metadata creation 
    create_metadata(user_id, pdf_id, pdf_path, quality_info)
    
    if quality_info['status'] == "UNSUPPORTED":
        raise HTTPException(
            status_code=400,
            detail="Scanned PDF not support yet"
        )
        
    return {
        "pdf_id" : pdf_id,
        "status": "INGESTED",
        "quality": quality_info["status"]
    }