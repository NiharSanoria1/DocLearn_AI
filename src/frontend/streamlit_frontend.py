import streamlit as st
import os
import sys
from uuid import uuid4
# 1. Get the path to the current folder (src/frontend)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to get the 'src' folder
src_dir = os.path.join(current_dir, '..')

# 3. Add 'src' to the Python path
sys.path.append(src_dir)

from backend.app.normal_chatbot.chatbot_backend import chatbot

from langchain_core.messages import HumanMessage
st.title("LLM Chatbot")

################################# SIDEBAR ################################
st.sidebar.title("Teaching Assistant")

st.sidebar.header("Conversations")


###################################################################################33


#******************************* Chat History *************************************

# initializing chat history list
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# printing chat history

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
#***********************************************************************************




if prompt := st.chat_input("write you question Here"):
    # display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # adding user message into the session state
    st.session_state.messages.append({"role": "user", "content": prompt})    
    
    CONFIG = {"configurable": {"thread_id": "1"}}
    
    # response = chatbot.stream(HumanMessage(content=prompt), config=CONFIG)
    # answer = response["messages"][-1].content
    #displaying llm output
    with st.chat_message("assistant"):
        ai_message =st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=prompt)]},
                
                config=CONFIG,
                stream_mode='messages'
            )
        )
    # adding ai answer to session state
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
            
        
 