import os
import json
from dotenv import load_dotenv
from typing import Dict
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

hf_api_key = os.getenv("HF_TOKEN")


def classify_question_intent(
    question: str,
    model_name: str = "meta-llama/Llama-3.1-8B-Instruct"
):
    """
    Classify question intent and extract key terms.
    """
    
    llm = HuggingFaceEndpoint(
        repo_id=model_name,
        task="text-generation",
        max_new_tokens=256,
        temperature=0.1,
        huggingfacehub_api_token=hf_api_key
    )
    
    chat_llm = ChatHuggingFace(llm=llm)
    
    prompt = f"""
    Analyze the user's question. Return ONLY a JSON object. Do not add markdown formatting.
    
    Question: "{question}"
    
    JSON Schema:
    {{
      "intent": "explain" | "define" | "compare" | "diagram" | "summarize",
      "key_terms": ["list", "of", "important", "nouns"],
      "mentions_image": boolean,
      "mentions_page": boolean
    }}
    """
    
    messages = [
        SystemMessage(content="You are a question intent classifier"),
        HumanMessage(content=prompt)
    ]
    
    response = chat_llm.invoke(messages)
    try:
        clean_json = response.content.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json.split("```json")[1].split("```")[0]
        parsed = json.loads(clean_json)
    except Exception as e:
        print(f"Intent parsing failed: {e}") # Debug log
        # fallback basic
        parsed = {
            "intent": "explain",
            "key_terms": question.lower().split(),
            "mentions_image": False,
            "mentions_page": False
        }
        
    return parsed