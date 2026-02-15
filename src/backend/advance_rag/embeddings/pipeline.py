from typing import List
import numpy as np

from app.embeddings.generator import get_embedding_model
from app.embeddings.vectorstore import FaissVectorStore


def run_phase8(
    chunks: List,
    pdf_id: str,
    embedding_model_name: str="BAAI/bge-large-en-v1.5",
    hf_api_key: str | None = None
):
    """
    Phase 8 : generate embeddings for ech chunk ans store in a vector DB.
    """
    
    embedder = get_embedding_model(
        model_name=embedding_model_name,
        hf_api_key=hf_api_key
    )
    
    store = FaissVectorStore(
        index_dir=f"data/vectors/{pdf_id}",
        dim=1024
    )
    store.load()
    
    embeddings = []
    metadatas = []
    
    for chunk in chunks:
        emb = embedder.embed_documents([chunk.text])[0]
        embeddings.append(np.array(emb))
        
        meta = {
            "pdf_id": pdf_id,
            "chunk_id": chunk.chunk_id,
            "unit_id": chunk.unit_id,
            "concept": chunk.concept,
            "page_numbers": chunk.page_numbers,
            "image_ids": chunk.image_ids,
            "anchor_type": chunk.metadata.get("anchor_type"),
            "source_type": chunk.metadata.get("source_type"),
            "text": chunk.text,
            "model": embedding_model_name
        }
        metadatas.append(meta)
        
    store.add(embeddings, metadatas)
    
    return store