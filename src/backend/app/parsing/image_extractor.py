import pdfplumber
import os
from pathlib import Path


def clamp_bbox(bbox, page_width, page_height):
    x0, top, x1, bottom = bbox

    x0 = max(0, x0)
    top = max(0, top)
    x1 = min(page_width, x1)
    bottom = min(page_height, bottom)

    # Ensure bbox is valid
    if x1 <= x0 or bottom <= top:
        return None

    return (x0, top, x1, bottom)


def extract_images_from_pdf(pdf_path: str, output_dir: str):
    
    """
    Extract images from PDF and save them page-wise
    Returns images metadata. 
    """    
    
    images_metadata =[]
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    with pdfplumber.open(pdf_path) as pdf:
        
        for page_index, page in enumerate(pdf.pages):
            page_number = page_index + 1
            
            for img_index, img in enumerate(page.images):
                #bounding box
                raw_bbox = (
                    img["x0"],
                    img["top"],
                    img["x1"],
                    img["bottom"],
                )
                
                bbox = clamp_bbox(raw_bbox, page.width, page.height)
                if bbox is None:
                    continue
                
                
                # cropping page to image box
                cropped_page = page.crop(bbox, strict=False)
                
                page_image = cropped_page.to_image(resolution=300)
                
                image_filename = f"page_{page_number}_img_{img_index +1}.png"
                image_path = Path(output_dir) / image_filename
                
                page_image.save(image_path)
                
                image_info = {
                    "page_number": page_number,
                    "image_index": img_index +1,
                    "file_path": str(image_path),
                    "bbox": bbox,
                    "width": img.get("width"),
                    "height": img.get("height"),
                    "dpi": 300
                }
                
                images_metadata.append(image_info)


    return images_metadata