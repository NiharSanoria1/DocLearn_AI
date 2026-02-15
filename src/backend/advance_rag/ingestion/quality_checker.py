import pdfplumber

def check_pdf_quality(pdf_path: str):
    
    total_pages = 0
    text_pages = 0
    image_only_pages =0
    
    with pdfplumber.open(pdf_path) as pdf:
        
        total_pages = len(pdf.pages)
        
        for page in pdf.pages:
            text = page.extract_text()
            images = page.images
            
            if len(text.strip())> 50 :
                text_pages +=1
            elif images:
                image_only_pages +=1
                
    if text_pages / total_pages >= 0.7:
        status = "SUPPORTED"
    elif text_pages >0 :
        status = "DEGRADED"
    else:
        status = "UNSUPPORTED"
        
    return {
        "status": status,
        "total_pages": total_pages,
        "text_pages": text_pages,
        "image_only_pages": image_only_pages
    }