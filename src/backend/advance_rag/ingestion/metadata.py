import json
from pathlib import Path
from datetime import datetime

def create_metadata(user_id: str, pdf_id: str, pdf_path: str, quality_info):
    
    meta = {
        "user_id": user_id,
        "pdf_id": pdf_id,
        "pdf_path": pdf_path,
        "uploaded_at": datetime.utcnow().isoformat(),
        "quality": quality_info            
        }
    
    meta_path = Path(pdf_path).parent / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent= 2)