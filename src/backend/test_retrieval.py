from pathlib import Path
import numpy as np

# ----------------------------
# Imports
# ----------------------------
from app.embeddings.generator import get_embedding_model
from app.embeddings.vectorstore import FaissVectorStore

# ----------------------------
# Config
# ----------------------------
pdf_id = "77573c06-3e83-4ab6-a3fb-f62987065c5a"
vector_dir = Path("data/vectors") / pdf_id

# ----------------------------
# Load existing vector store
# ----------------------------
print(f"🔍 Loading vector store for PDF: {pdf_id}")
store = FaissVectorStore(index_dir=str(vector_dir), dim=1024)

# Manually load (no regeneration)
try:
    store.load()
    print("✔ Vector store loaded successfully!")
except Exception as e:
    print("❌ Failed to load vector store:", e)
    exit(1)

# ----------------------------
# Create Embedding Model
# ----------------------------
print("\n🔍 Initializing embedding model")
embedder = get_embedding_model(model_name="BAAI/bge-large-en-v1.5")

# ----------------------------
# Define query
# ----------------------------
query = input("\nEnter query: ")

# ----------------------------
# Embed query
# ----------------------------
print("\n▶ Computing query embedding")
query_emb = embedder.embed_query(query)

# ----------------------------
# Perform semantic search
# ----------------------------
print("\n▶ Retrieving top chunks")
results = store.query(np.array([query_emb]), k=5)

# ----------------------------
# Print results
# ----------------------------
print(f"\n📌 Top results for query:\n   \"{query}\"\n")
for idx, r in enumerate(results, start=1):
    print(f"{idx}. Chunk ID: {r['chunk_id']}")
    print(f"   Concept:   {r['concept']}")
    print(f"   Page nums: {r['page_numbers']}")
    print(f"   Text snippet: {r['text'][:200]}...\n")
