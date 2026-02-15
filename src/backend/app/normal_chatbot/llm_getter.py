from langchain_huggingface import (ChatHuggingFace, HuggingFaceEndpoint, 
                                   HuggingFaceEndpointEmbeddings)
import os
from dotenv import load_dotenv

load_dotenv()


def get_embedding_model(
    model_name: str = "BAAI/bge-large-en-v1.5" ,
    hf_api_key : str = None
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

def get_chating_model(
    model_name : str ="Qwen/Qwen3-VL-8B-Instruct",
    hf_api_key : str = None
):
    """ Generate and returns the chat model endpont """
    
    resolved_key = hf_api_key or os.getenv("HF_TOKEN")
    if not resolved_key:
        raise ValueError("Hugging Face API key not found in args or environment.")
    
    llm = HuggingFaceEndpoint(
        repo_id=model_name,
        task="text2text",
        huggingfacehub_api_token=resolved_key,
        temperature= 0.4
    )
    
    return ChatHuggingFace(llm = llm)


if __name__=="__main__":
    model = get_chating_model()
    
    print(model.invoke("hi"))