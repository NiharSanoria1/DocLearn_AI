from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_embedding_model(
    model_name : str="BAAI/bge-large-en-v1.5",
    hf_api_key: str=None
):
    """
    Initialize embedding model for BAAI/bge-large-en-v1.5 (1024 dim).
    """
    
    resolved_key = hf_api_key or os.getenv("HF_TOKEN")

    if not resolved_key:
        raise ValueError("Hugging Face API key not found in args or environment.")
    
    return HuggingFaceEndpointEmbeddings(
        model=model_name,
        huggingfacehub_api_token= resolved_key,
        task="feature-extraction"
        # model_name=model_name,
        # api_key=hf_api_key
    )
    