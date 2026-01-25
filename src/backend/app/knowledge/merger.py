from app.knowledge.schemas import TextSource, ImageSource, LearningUnit
from app.knowledge.scoring import text_strength, image_strength, extract_candidate_concepts


def decide_anchor(texts: list[TextSource], images: list[ImageSource]):
    """
    text strength vs image strength accross all scores
    """
    
    ts = sum(text_strength(t.text) for t in texts)
    is_ = sum(image_strength(i.explanation) for i in images)
    
    if is_ > ts * 1.2:
        return "image"
    elif ts > is_ * 1.2:
        return "text"
    return "hybrid"




def merge_learning_unit(
    page_number: int,
    raw_text: str,
    image_explanations: list[dict]
) -> LearningUnit:
    
    """ For a simgle page concept cluster merge page text and image explanations"""
    
    #wrap
    text_sources = [TextSource(page_number=page_number, text= raw_text)]
    
    image_sources = [
        ImageSource(
            image_id=img["image_id"],
            page_number = img["page_number"],
            explanation= img["explanation"]
        ) for img in image_explanations
    ]
    
    # extract candidate concepts
    image_concepts_flat = []
    for img in image_explanations:
        image_concepts_flat += img.get("concepts", [])
        
    # text concepts
    concepts = extract_candidate_concepts(raw_text, image_concepts_flat)
    
    anchor = decide_anchor(text_sources, image_sources)
    
    unit_id = f"page_{page_number}_{anchor}"
    
    # combine explanation heuristically
    combined = ""
    if anchor in ["image", "hybrid"]:
        combined += "Image Explanation: " + " ".join(
            i.explanation for i in image_sources
        ) + "\n"
        
    if anchor in ["text", "hybrid"]:
        combined += "Text Excerpt: " + raw_text 
        
    # fallback
    if not combined.strip():
        combined = raw_text or "No Context"
        
    return LearningUnit(
        unit_id=unit_id,
        anchor_type=anchor,
        title = f"Concepts on page {page_number}",
        concepts=concepts,
        text_sources = text_sources,
        image_sources = image_sources,
        combined_explanation=combined.strip(),
        grounding={
            "pages": [page_number],
            "images" : [i.image_id for i in image_sources]
        }
    )
    
     
    