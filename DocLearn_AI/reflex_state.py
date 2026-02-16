import os, sys
import asyncio
# 1. Get the path to the current folder (src/frontend)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to get the 'src' folder
src_dir = os.path.join(current_dir, '..')

# 3. Add 'src' to the Python path
sys.path.append(src_dir)

# state.py
import reflex as rx
from uuid import uuid4
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from src.backend.app.normal_chatbot.chatbot_backend import workflow, llm

# langgraph config
# CONFIG = {"configurable": {"thread_id": "1"}}
    

class State(rx.State):
    #-----UI STATE------
    
    # --- SIDEBAR STATE ---
    sidebar_open: bool = True  # Default to open
    
    # The current question being asked.
    question: str = ""
    # Keep track of the chat history as a list of (question, answer) tuples.
    chat_history: list[tuple[str, str]] =[]

    #-----SESSION STATE------
    #session management
    thread_id : str = "" # starting with a random id
    chat_sessions : list[dict[str,str]] = [] # list of available thread Id's
    last_active_thread: str = rx.Cookie(name="last_active_thread") # remembers the last chat the user was looking at
    
    #---USER AUTH----
    user_token: str = rx.Cookie(name="user_token")
    
    #-----REMAINING STATE------
    editing_chat_id: str =""
    new_chat_title :str =""
    is_renaming: bool = False
    
    #---- setters------
    def set_question(self, value: str):
        self.question = value
    
    def set_new_chat_title(self, value: str):
        self.new_chat_title = value
    
    def set_is_renaming(self, value: bool):
        self.is_renaming = value
    
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open
        
    #user related state
    def ensure_user_token(self):
        """If a user has no cookie , give them a new ID"""
        if not self.user_token:
            self.user_token = str(uuid4())
            # print(f"New user assigned: {self.user_token}")# for debugging
            
    async def _ensure_ownership_table(self, conn):
        """Create table that links user to threads"""
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS user_ownership(
                user_id TEXT,
                thread_id TEXT,
                title TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, thread_id)
            )
        """)
        await conn.commit()
    
    async def _generate_title(self, first_question: str) -> str:
        """Asks LLM to sumarize the first question to an title"""
        try: 
            #prompt for title generation
            messages = [
             SystemMessage(content="You are a chat title generator. Generate a concise (3-5 words) title for this user query. Do not use quotes."),
             HumanMessage(content=first_question)   
            ]
            response = await llm.ainvoke(messages) # using async invoke
            return response.content.strip()
        except Exception:
            return "New Chat"
        
    # helper load messages (used by on_load and select_chat)
    async def _load_messages_from_db(self):
        """Restores history for current self.thread_id"""
        self.chat_history = []
        db_path = "chatbot_database.db"
        config = {"configurable": {"thread_id": self.thread_id}}
        
        try:
            async with aiosqlite.connect(db_path, check_same_thread=False) as conn:
                checkpointer = AsyncSqliteSaver(conn=conn)
                chatbot = workflow.compile(checkpointer=checkpointer)
                
                snapshot= await chatbot.aget_state(config)
                if snapshot.values and "messages" in snapshot.values:
                    self.chat_history = self._parse_messages_to_history(snapshot.values["messages"])
        except Exception as e:
            print(f"Error loading chat: {e}")
    
    @rx.event
    async def fetch_chat_sessions(self):
        """ Load only the chats belonging to this user"""
        self.ensure_user_token()
        
        # This tells the browser: "Keep this cookie for 1 year (31536000 seconds)"
        # even if the user closes the window.
        # We tell the browser: "Set this cookie to expire in 1 year using js"
        yield rx.call_script(f"document.cookie = 'user_token={self.user_token}; max-age=31536000; path=/'")        
        # to ensure every user get new unique id
        # if not self.thread_id:
        #     self.thread_id= str(uuid4())
        
        db_path = "chatbot_database.db"
        if not os.path.exists(db_path):
            self.chat_sessions = []
            return 
        
        try :
            async with aiosqlite.connect(db_path) as conn:
                
                # creating ownership table if not present
                await self._ensure_ownership_table(conn)
                #only select threads linked to this user_token                
                cursor = await conn.execute(
                    "SELECT thread_id, title FROM user_ownership WHERE user_id = ? ORDER BY created_at DESC",
                    (self.user_token,)
                    )
                rows = await cursor.fetchall()
                # storing the ids in the list (reverse so newest might appear top if sorted by time)
                self.chat_sessions = [{"id" : row[0], "title": row[1] or "New Chat"} for row in rows]
        
        except Exception as e:
            print(f"Error fetching chats: {e}")
            
        # restore last state
        # If we have a cookie for the last thread, and it exists in our list, load it.
        session_ids = [s["id"] for s in self.chat_sessions]
        
        if self.last_active_thread and self.last_active_thread in session_ids:
            self.thread_id = self.last_active_thread
            await self._load_messages_from_db()
        else:
            self.thread_id = str(uuid4())
            self.chat_history = []
        yield 
        await asyncio.sleep(0.01)
        # This forces the browser to jump to the 'chat-end' ID
        yield rx.scroll_to("chat-end")
    
    @rx.event
    async def create_new_chat(self):
        """Generate new session and clears screen"""
        self.thread_id = str(uuid4())
        self.chat_history = []
        self.last_active_thread = self.thread_id
        yield rx.set_focus("question_input") # focus input box
        
    @rx.event
    async def delete_chat(self, chat_id_to_delete: str):
        """Remove a chat from DB and Sidebar"""
        # removing from local list 
        self.chat_sessions = [c for c in self.chat_sessions if c["id"] != chat_id_to_delete]
        
        # if we delete the active chat, reset the screen
        if self.thread_id == chat_id_to_delete:
            self.create_new_chat()
            
        # delete from DB
        db_path = "chatbot_database.db"
        try: 
            async with aiosqlite.connect(db_path) as conn:
                await conn.execute(
                    "DELETE FROM user_ownership WHERE thread_id =? AND user_id =?",
                    (chat_id_to_delete, self.user_token)
                )
                await conn.commit()
        except Exception as e:
            print(f"Error deleting: {e}")
            
    #-----------rename chat logic------------
    @rx.event
    def start_renaming(self, chat_id: str, current_title: str):
        self.editing_chat_id = chat_id
        self.new_chat_title = current_title
        self.is_renaming = True
    
    @rx.event
    def cancel_renaming(self):
        self.is_renaming = False
        
    @rx.event
    async def save_chat_title(self):
        """Update the title in the Db and UI"""
        #updating local list
        for chat in self.chat_sessions:
            if chat["id"] == self.editing_chat_id:
                chat["title"] = self.new_chat_title
                break
        
        # updating db
        db_path = "chatbot_database.db"
        try:
            async with aiosqlite.connect(db_path) as conn:
                await conn.execute(
                    "UPDATE user_ownership SET title = ? WHERE thread_id = ? AND user_id = ?",
                    (self.new_chat_title, self.editing_chat_id, self.user_token)
                )
        except Exception as e:
            print(f"Error renaming: {e}")
            
        self.is_renaming = False
    
    @rx.event
    async def select_chat(self, selected_thread_id: str):
        """ Loads a specific chat from history """
        # update the active id
        self.thread_id = selected_thread_id
        self.last_active_thread = selected_thread_id
        # clear history immediately (visual feedback)
        self.chat_history = []
        yield 
        
        #load data
        await self._load_messages_from_db()
        yield
        await asyncio.sleep(0.01)
        yield rx.scroll_to("chat-end")
        
    
    def _parse_messages_to_history(self, messages):
        """Helper to convert LangChain Messages to reflex UI format"""
        history =[]
        current_pair = [None, None] # [Question, Answer]
        
        for msg in messages:
            if isinstance(msg, HumanMessage):
                current_pair[0] = msg.content
            elif isinstance(msg, AIMessage):
                current_pair[1] = msg.content
                
                # once we have both add to history and reset
                if current_pair[0] is not None:
                    history.append(tuple(current_pair))
                    current_pair = [None, None]
        
        return history
    
    @rx.event
    async def handle_form_submit(self, form_data: dict):
        """
        Gets text from the form, update state, and runs answer generator.
        """
        # get text using the id we set in the doclearn_ai.py
        user_text = form_data.get("question_box")
        
        if not user_text or user_text.strip() =="":
            return 
        
        # update state variable manually
        self.question = user_text
        
        async for update in self.answer():
            yield update
                
    @rx.event
    async def answer(self):
        
        self.ensure_user_token()
        self.last_active_thread = self.thread_id
        
        user_question = self.question
        self.question = ""        
        # checking id against list of dicts
        is_new_thread = self.thread_id not in [c["id"] for c in self.chat_sessions] 

        
        # Add question + empty placeholder for answer
        self.chat_history.append((user_question, ""))
        yield
        yield rx.scroll_to("chat-end")
        
        inputs = {"messages": [HumanMessage(content=user_question)]}
        config = {"configurable" : {"thread_id": self.thread_id}}
        db_path = "chatbot_database.db"
                
        try:
            async with aiosqlite.connect(db_path, check_same_thread = False) as conn:
                await self._ensure_ownership_table(conn)
                
                # inserting user ownership record                
                if is_new_thread:
                    # generating title usning llm
                    generated_title = await self._generate_title(user_question)
                    await conn.execute(
                        "INSERT OR IGNORE INTO user_ownership (user_id, thread_id, title) VALUES (?, ?, ?)",
                        (self.user_token, self.thread_id, generated_title)
                    )
                    await conn.commit()
                    
                    #update local list so sidebar shows it immediately
                    self.chat_sessions.insert(0, {"id": self.thread_id, "title": generated_title})
                    yield # triger sidebar refresh
                
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
            self.chat_history[-1] = (user_question, f"Error: {e}")
            yield
            yield rx.scroll_to("chat-end")