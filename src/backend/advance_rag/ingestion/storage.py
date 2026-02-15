import os
from pathlib import Path
import shutil

BASE_PATH = Path("data/raw")

def save_pdf(user_id: str, pdf_id: str, file):
    
    pdf_dir = BASE_PATH / user_id / pdf_id
    pdf_dir.mkdir(parents=dir, exist_ok=True)
    
    pdf_path = pdf_dir / "original.pdf"
    
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
        
    file.file.seek(0)
    return str(pdf_path)
