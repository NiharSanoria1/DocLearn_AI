from pydantic import BaseModel
from typing import  Annotated

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class ChattingSchema(BaseModel):
    
    # session_id: str
    # user_id: str
    messages: Annotated[list[BaseMessage], add_messages]