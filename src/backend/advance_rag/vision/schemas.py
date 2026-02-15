from typing import List, Optional
from pydantic import BaseModel

class ImageExplanation(BaseModel):
    image_id : str
    page_number: int
    
    
    image_type: str
    importance: str
    
    concepts: List[str]
    
    visual_description: str
    explanation: str
    
    teaching_notes: Optional[str] = None
    limitations: Optional[str] = None
    
# print("all ok")

class ImageExplanation(BaseModel):
    image_id: str
    page_number: int
    
    #metadata not produced by model
    image_type: str = "diagram"
    importance: str = "high"

    visual_description: str
    explanation: str
    concepts: List[str]
    
    teaching_notes: Optional[List[str]] = None
    limitations: Optional[str] = None