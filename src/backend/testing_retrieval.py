from app.retrieval.pipeline import retrieve_relevant_chunks

pdf_id = "80f241f5-f098-4d93-b79b-f15a933b4f7a"

question = "what is reinforcement learning"

result = retrieve_relevant_chunks(
    question=question,
    pdf_id=pdf_id
)

print("\n🧠 INTENT")
print(result["intent"])

print("\n📌 SELECTED CHUNKS\n")
for i, c in enumerate(result["chunks"], 1):
    print(f"{i}. {c['chunk_id']}")
    print(f"   Concept: {c.get('concept')}")
    print(f"   Pages: {c.get('page_numbers')}")
    print(f"   Text: {c['text'][:200]}...\n")