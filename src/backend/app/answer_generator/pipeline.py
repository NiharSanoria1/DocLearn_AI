import os 
from typing import List, Dict

from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

hf_api_key = os.getenv("HF_TOKEN")

# phase 11: rag answer generation

def generate_answer(
    question: str,
    intent: str,
    chunks: List[Dict],
    model_name: str = "meta-llama/Llama-3.1-8B-Instruct",
    max_new_tokens: int = 512,
    temperature: float = 0.1
) -> str:
    """
    Combine retrieved chunks into grounded answer using LLM.
    
    Rules:
    - Answer ONLY from the provided context
    - cite page numbers in the answer
    - If missing critical context, respond with a safe refusal.
    """
    
    # 1 building the grounded context block
    context_blocks = []
    for c in chunks:
        pages = c.get("pages") or c.get("page_numbers") or []
        pages_str= ", ".join(str(p) for p in pages)
        text = c.get("text", "").strip()
        # attach pages in paranthesis
        context_blocks.append(f"(Page {pages_str}) {text}")
        
    # joining them into a single context text
    context_text = "\n\n".join(context_blocks).strip()
    
    # for debugging *******************
    
    print("DEBUG CONTEXT:\n", context_text[:1000])
    print("DEBUG CHUNKS:", [c["chunk_id"] for c in chunks])

    # ***************************
    
    # 2 constructing the block
    
    system_prompt = (
        "You are an academic tutor and knowledge engine.\n"
        "Answer the user’s question using ONLY the provided contextual text.\n"
        "Cite page numbers for every fact you provide.\n"
        "Do NOT use any outside knowledge.\n"
        "If the context does not contain sufficient information to answer, "
        "respond: 'Not found in this PDF.'\n"
        "Do not add explanations beyond the provided context.\n"
    )

    human_prompt = f"""
                    Question:
                    {question}

                    Context:
                    {context_text}
                    Please:
                    - Write a complete definition of the concept
                    - Include how the main components relate
                    - Cite page numbers for each statement
                    
                    Answer rules:
                    1. Start with a 1-2 sentence definition
                    2. Explain components step-by-step
                    3. Use bullet points where possible
                    4. Cite page numbers after each section
                    5. Do not repeat the same page twice unless necessary
                    Answer below:
                """
                
    # 3 initializing the llm
    llm =HuggingFaceEndpoint(
        repo_id=model_name,
        task="text-generation",
        max_new_tokens=max_new_tokens,
        temperature=temperature,
        huggingfacehub_api_token=hf_api_key,
        provider="cerebras"
    )
    
    chat_llm = ChatHuggingFace(llm=llm)
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]
    
    response = chat_llm.invoke(messages)
    answer_text = response.content.strip()
    
    return answer_text
    