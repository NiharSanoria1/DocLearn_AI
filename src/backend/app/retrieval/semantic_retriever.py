import numpy as np
from app.embeddings.generator import get_embedding_model
from app.embeddings.vectorstore import FaissVectorStore
from typing import List

class SemanticRetriever:
    def __init__(self, pdf_id: str, embedding_model: str = "BAAI/bge-large-en-v1.5"):
        self.pdf_id = pdf_id
        self.store = FaissVectorStore(f"data/vectors/{pdf_id}", dim=1024)
        self.store.load()
        self.embedder = get_embedding_model(model_name=embedding_model)
        
    def retrieve(
        self,
        query : str,
        top_k: int = 20
    ) -> List[dict]:
        # embed
        query_emb = self.embedder.embed_query(query)
        # search
        results = self.store.query(np.array([query_emb]), k = top_k)
        return results

