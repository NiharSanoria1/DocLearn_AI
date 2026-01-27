from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import HumanMessage, SystemMessage
from PIL import Image
import base64
from io import BytesIO

from app.vision.schemas import ImageExplanation
from app.vision.prompt import USER_PROMPT_TEMPLATE, SYSTEM_PROMPT
from dotenv import load_dotenv
import os
load_dotenv()

huggingface_api_key = os.getenv("HF_TOKEN")


def image_to_base64(image_path: str) -> str:
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")


def get_vision_model():
    """
    Returns a LangChain wrapper for Llama-3.2-90B-Vision-Instruct
    """
    llm = HuggingFaceEndpoint(
        
        repo_id="Qwen/Qwen3-VL-8B-Instruct",
        task= "image-text-to-text",
        temperature=0.3,
        max_new_tokens=512
    ) 
    
    return ChatHuggingFace(llm=llm)

def explain_image(
    image_path: str,
    page_text: str,
    image_id: str,
    page_number: int
) -> ImageExplanation:
    
    """Sends image and context to vision model and returns explanation."""
    
    model = get_vision_model()
    
    image_base64 = image_to_base64(image_path)
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {"type": "text",
                 "text": USER_PROMPT_TEMPLATE.format(page_text=page_text)
                },
                {"type": "image_url", 
                 "image_url":{
                     
                    "url": f"data:image/png;base64, {image_base64}"
                    
                    }
                }
            ]
        )
    ]
    
    response = model.invoke(messages)
    
    raw_text = response.content
    
    return {
        "image_id": image_id,
        "page_number": page_number,
        "raw_explanation" : raw_text
    }