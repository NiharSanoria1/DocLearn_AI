import os
import pickle
from pathlib import Path
import faiss
import numpy as np

class FaissVectorStore:
    def __init__(self, index_dir: str, dim: int=1024):
        self.index_dir = Path(index_dir)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        
        self.faiss_index = None
        self.metadata = []
        self.dim = dim
        
    def _index_path(self):
        return self.index_dir / "index.faiss"
    
    def _meta_path(self):
        return self.index_dir / "metadata.pkl"
    
    def load(self):
        if self._index_path().exists():
            self.faiss_index = faiss.read_index(str(self._index_path()))
            with open(self._meta_path(), "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.faiss_index = faiss.IndexFlatIP(self.dim)
    
    def save(self):
        faiss.write_index(self.faiss_index, str(self._index_path()))
        with open(self._meta_path(), "wb") as f:
            pickle.dump(self.metadata, f)
            
    def add(self, embeddings: list[np.ndarray], metadatas: list[dict]):
        if self.faiss_index is None:
            self.load()
            
        X = np.vstack(embeddings).astype("float32")
        self.faiss_index.add(X)
        self.metadata.extend(metadatas)
        self.save()
        
    def query(self, embedding: np.ndarray, k: int=5):
        D, I = self.faiss_index.search(embedding.astype("float32"), k)
        results = []
        for idx_list in I:
            for idx in idx_list:
                results.append(self.metadata[idx])
        return results
            
            
                