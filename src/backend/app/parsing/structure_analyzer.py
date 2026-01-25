import pdfplumber
import json
from pathlib import Path

def analyze_pdf_structure(pdf_path: str):
    """"Analyse pdf page by page and return structure information"""
    
    pages_structure = []
    
    with pdfplumber.open(pdf_path) as pdf:
        
        total_pages = len(pdf.pages)
        
        for idx, page in enumerate(pdf.pages):
            page_number = idx +1
            
            raw_text = page.extract_text() or ""
            
            images_data = []
            
            for img in page.images:
                images_data.append({
                    "width": img.get("width"),
                    "height": img.get("height"),
                    "bbox":(
                        img.get("x0"),
                        img.get("top"),
                        img.get("x1"),
                        img.get("bottom")
                    )
                })
            
            page_data = {
                "page_number": page_number,
                "width": page.width,
                "height": page.height,
                "text" : raw_text,
                "images": images_data
            }
            
            pages_structure.append(page_data)
            
            
    return pages_structure