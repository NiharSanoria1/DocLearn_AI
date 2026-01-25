

def should_explain_image(image_meta: dict, page_text: str) -> bool:
    """
    Decide whether an image should be sent to a vision-model for explanation.
    """
    width = image_meta.get("width",0)
    height = image_meta.get("height", 0)
    
    area = width * height
    
    # rule 1: skip very small images
    if area < 15000:
        return False
    
    # rule 2: skip extreamly thin images (banners, lines)
    aspect_ratio = max(width, height)/ max(1, min(width, height))
    if aspect_ratio > 8: 
        return False
    
    # rule3: skip short-height strips (formulas, banners)
    if height < 90:
        return False
    
    # page context gate
    if (len(page_text.strip()))< 30:
        return True
    
    return True