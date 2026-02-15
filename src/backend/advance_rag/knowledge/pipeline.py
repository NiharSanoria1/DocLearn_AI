from app.knowledge.merger import merge_learning_unit
from app.vision.storage import load_image_explanations
from app.parsing.text_normalizer import normalize_text_pages

def run_phase6(
    raw_pages: list,
    image_explanations: list,
    pdf_id: str
): 
    """
    raw_pages: output of Phase 3
    image_explanations: output of Phase 5 storage
    """

    # for storage of units
    all_units = []
    
    # grouping explanations by page
    images_by_page = {}
    for ie in image_explanations:
        images_by_page.setdefault(ie["page_number"], []).append(ie)
    
    for page in raw_pages:
        pn = page["page_number"]
        raw_text = page["clean_text"]
        
        page_imgs  = images_by_page.get(pn,[])
        
        unit = merge_learning_unit(pn, raw_text, page_imgs)
        all_units.append(unit)
        
    return all_units    
        