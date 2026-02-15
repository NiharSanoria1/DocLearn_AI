from typing import List
import re
import uuid

from app.chunking.schemas import ChunkSchema
# from app.chunking.prompt import prompt

# llm import
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage



# rule based splitting 
def simple_rule_split(
    unit_id: str,
    combined_text: str,
    page_numbers: List[int],
    image_ids: List[str],
    metadata: dict
) -> List[ChunkSchema]:
    """
    Rule-based chunker: splits text on blank lines or double newlines.
    """
    
    parts = [p.strip() for p in re.split(r"\n\s*\n+", combined_text) if p.strip()]
    
    chunks = []
    for i, part in enumerate(parts):
        #using first word as naive concept
        concept = part.split(".")[0][:50]
        chunk_id = f"{unit_id}_rule_{i}_{uuid.uuid4().hex[:6]}"
        chunks.append(ChunkSchema(
            chunk_id=chunk_id,
            unit_id=unit_id,
            concept=concept,
            text= part,
            page_numbers=page_numbers,
            image_ids=image_ids,
            metadata=metadata
        ))
        
    # if no splits are found, return the whole text as a single chunk
    if not chunks:
        chunks= [ChunkSchema(
            chunk_id=f"{unit_id}_rule_0_{uuid.uuid4().hex[:6]}",
            unit_id=unit_id,
            concept=combined_text[:30],
            text=combined_text,
            page_numbers=page_numbers,
            image_ids=image_ids,
            metadata=metadata
        )]
    
    return chunks

# LLM based splitting (fallback)
def llm_chunk_split(
    unit_id: str,
    text: str,
    page_numbers: List[int],
    image_ids: List[str],
    metadata: dict,
    model_name: str = "Qwen/Qwen3-VL-8B-Instruct" #"google/gemma-3-27b-it"
) -> ChunkSchema:
    
    """
    Uses an LLM to split text into semantically coherent chunks.
    """
    # creating hf based llm
    llm = ChatHuggingFace(
        llm= HuggingFaceEndpoint(
            repo_id=model_name,
            task="text2text",
            temperature=0.4,
            max_new_tokens=600
        )
    )
    # Prompt to ask LLM to split text
    prompt = f"""
                Split the text below into concept chunks. For each chunk,
                produce a short "concept" and the "text" describing that concept.
                Return EXACTLY a JSON array of objects like:
                [
                  {{ "concept": "...", "text": "..." }},
                  ...
                ]

                Text to split:
                \"\"\"
                {text}
                \"\"\"
                """
    messages = [
        SystemMessage(content="You are a chunking assistant."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    raw = response.content.strip()
    
    #try to parse json, fallback to rule-based
    import json
    try:
        data = json.loads(raw)
    except Exception:
        # if parsing fails, fallback
        return simple_rule_split(unit_id, text, page_numbers, image_ids, metadata)
    
    chunks= []
    for idx, obj in enumerate(data):
        concept = obj.get("concept", "").strip()
        chunk_text = obj.get("text", "").strip()
        if not chunk_text:
            continue
        
        chunk_id = f"{unit_id}_llm_{idx}_{uuid.uuid4().hex[:6]}"
        chunks.append(ChunkSchema(
            chunk_id=chunk_id,
            unit_id=unit_id,
            concept=concept,
            text=chunk_text,
            page_numbers=page_numbers,
            image_ids=image_ids,
            metadata=metadata
        ))
     
    # if llm returned nothing, fallback
    if not chunks:
        return simple_rule_split(unit_id, text, page_numbers, image_ids, metadata)
    
    return chunks

# hybrid splitter function
def hybrid_split(
    unit_id: str,
    text: str,
    page_numbers: List[int],
    image_ids: List[str],
    metadata: dict,
    use_llm: bool = True
) -> List[ChunkSchema]:
    """
    Hybrid splitting strategy:
    - First try rule-based splitting.
    - If this yields a single chunk AND text is long, then use LLM splitting.
    """
    
    # always doing rule based first
    rule_chunks = simple_rule_split(unit_id, text, page_numbers, image_ids, metadata)
    
    #decide to fallback or not
    needs_llm = False
    if len(rule_chunks)<=1:
        # if rule creates only 1 chunk and text is substantil
        word_count = len(text.split())
        if word_count > 200 and use_llm:
            needs_llm = True
    
    if needs_llm:
        return llm_chunk_split(unit_id, text, page_numbers, image_ids, metadata)
    
    return rule_chunks
    