# from fastapi import FastAPI, HTTPException, UploadFile, File
# from uuid import uuid4

# # from app.api.routes.upload import router as upload_router
# from app.ingestion.pdf_validator import validate_pdf
# from app.ingestion.storage import save_pdf
# from app.ingestion.quality_checker import check_pdf_quality
# from app.ingestion.metadata import create_metadata

# app = FastAPI()

# @app.get("/")
# def health_check():
#     return {"status": "ok"}

# @app.post("/upload-test")
# async def upload_pdf(file: UploadFile = File(...)):
    
#     user_id = "test_user"
#     pdf_id = str(uuid4())
    
#     validate_pdf(file)
    
#     pdf_path  = save_pdf(user_id, pdf_id, file)
    
#     quality_report = check_pdf_quality(pdf_path)
    
#     create_metadata(user_id, pdf_id, pdf_path, quality_report)
    
#     return {
#         "message": "PDF validated and stored successfully",
#         "pdf_id": pdf_id,
#         "stored_at": pdf_path,
#         "status": quality_report["status"]
#     } 



# result = explain_image(
#     image_path="data/processed/test_user/80f241f5-f098-4d93-b79b-f15a933b4f7a/images/page_8_img_1.png",
#     page_text="Action-Reward feedback loop ...",
#     image_id="page_8_img_1",
#     page_number=8
# )


from backend.app.normal_chatbot.chatbot_backend import chatbot 
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id": "1"}}

response = chatbot.invoke({"messages": HumanMessage(content="what is the best porn site ?")}, config=CONFIG)
print(response["messages"][-1].content)