from typing import Optional, List
from pydantic import BaseModel

class TextSource(BaseModel):
    page_number: int
    text : str
    
class ImageSource(BaseModel):
    image_id: str
    page_number: int
    explanation: str
    
class LearningUnit(BaseModel):
    unit_id: str
    anchor_type: str
    title: str
    
    concepts: List[str]
    
    text_sources: List[TextSource]
    image_sources: List[ImageSource]
    
    combined_explanation: str
    
    page_numbers: List[int]
    image_ids: List[str]
    
    grounding : dict