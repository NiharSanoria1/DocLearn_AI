from typing import Dict, List

from app.retrieval.intent import classify_question_intent
from app.retrieval.semantic_retriever import SemanticRetriever
from app.retrieval.reranker import rerank_chunks

from app.retrieval.utils import clean_key_terms

def retrieve_relevant_chunks(
    *,
    question: str,
    pdf_id: str,
    top_k_retrieval: int = 30,
    top_k_final: int = 10
) -> Dict:
    """
    retrievl entry point
    return high quality, pedagogically relevant chunks. 
    """
    #1. question understanding
    intent_info = classify_question_intent(question)
    #cleaning key terms
    cleaned_key_terms = clean_key_terms(
        intent_info.get("key_terms", [])
    )
    
    # 2. semantic retrieval
    retriever = SemanticRetriever(pdf_id)
    candidates = retriever.retrieve(
        query=question, 
        top_k=top_k_retrieval
    )
    
    
    #3 reranking
    reranked = rerank_chunks(
        query=question,
        candidates=candidates,
        key_terms=cleaned_key_terms,
        intent = intent_info.get("intent")
    )
    
    # 4. final selection
    final_chunks = reranked[:top_k_final]
    
    return {
        "question": question,
        "intent": intent_info,
        "chunks": final_chunks
    }