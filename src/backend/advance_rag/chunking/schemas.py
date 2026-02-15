from typing import List, Optional
from pydantic import BaseModel

class ChunkSchema(BaseModel):
    chunk_id: str
    unit_id: str
    concept: str
    text: str
    
    page_numbers: List[int]
    image_ids: List[str]
    
    metadata : dict