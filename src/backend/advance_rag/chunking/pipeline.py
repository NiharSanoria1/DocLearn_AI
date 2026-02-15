from typing import List
from app.chunking.schemas import ChunkSchema
from app.chunking.splitter import hybrid_split
from app.knowledge.schemas import LearningUnit

def chunk_learning_unit(
    unit: LearningUnit,
    use_llm: bool = True
) -> List[ChunkSchema]:
    """
    Hybrid chunking for one learning unit.
    """
    
    text = unit.combined_explanation
    page_nums = unit.page_numbers
    image_ids = unit.image_ids
    metadata = {
        "anchor_type": unit.anchor_type,
        "source_type": "multimodel" if unit.image_ids else "text"
    }
    return hybrid_split(
        unit.unit_id,
        text,
        page_nums,
        image_ids,
        metadata,
        use_llm=use_llm
    )
    
def run_phase7(
    learning_units: List[LearningUnit],
    use_llm: bool = True
) -> List[ChunkSchema]:
    """
    Run chunking phase (phase 7) on all learning units.
    """
    all_chunks : List[ChunkSchema] = []
    
    for unit in learning_units:
        unit_chunks = chunk_learning_unit(unit, use_llm=use_llm)
        all_chunks.extend(unit_chunks)
        
    return all_chunks
   