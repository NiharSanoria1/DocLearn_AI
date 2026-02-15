import os, sys
# 1. Get the path to the current folder (src/frontend)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to get the 'src' folder
src_dir = os.path.join(current_dir, '..')

# 3. Add 'src' to the Python path
sys.path.append(src_dir)

# state.py
import reflex as rx

import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage
from src.backend.app.normal_chatbot.chatbot_backend import workflow

# langgraph config
# CONFIG = {"configurable": {"thread_id": "1"}}
    

class State(rx.State):

    # The current question being asked.
    question: str = ""

    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]] =[]

    thread_id : str = "user_session_1"
    
    @rx.event
    async def answer(self):
        
        user_question = self.question
        self.question = ""        
        yield 
        
        # Add question + empty placeholder for answer
        self.chat_history.append((self.question, ""))
        yield
        yield rx.scroll_to("chat-end")
        
        inputs = {"messages": [HumanMessage(content=user_question)]}
        config = {"configurable" : {"thread_id": self.thread_id}}
        
        db_path = "chatbot_database.db"
        
        try:
            async with aiosqlite.connect(db_path, check_same_thread = False) as conn:
                checkpointer = AsyncSqliteSaver(conn =conn)
                
                chatbot = workflow.compile(checkpointer=checkpointer)
                
                full_response = ""
                
                async for event in chatbot.astream_events(inputs, version='v2', config= config):

                    kind  = event["event"]

                    if kind == "on_chat_model_stream":
                        # 'chunk' is the piece of text (or message chunk)
                        chunk = event["data"]["chunk"]

                        # Check if the chunk has content (sometimes it's empty metadata)
                        if chunk.content :
                            # append content
                            full_response += chunk.content

                            # updating the reflex state
                            self.chat_history[-1] = (user_question, full_response)

                            # Trigger UI Update
                            yield
                            yield rx.scroll_to("chat-end")
        except Exception as e:
            print(f"streaming error : {e}")
            yield
            yield rx.scroll_to("chat-end")