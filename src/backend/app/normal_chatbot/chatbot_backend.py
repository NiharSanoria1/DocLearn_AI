from langgraph.graph import StateGraph, START, END

from src.backend.app.normal_chatbot.llm_getter import get_chating_model
from src.backend.app.normal_chatbot.schemas import ChattingSchema


llm = get_chating_model()
# *********************************** GRAPG NODES START****************************************************

def chat_node(state : ChattingSchema):
    
    messages = state.messages
    response = llm.invoke(messages)
    return {"messages": [response]}
    

# *********************************** GRAPH NODE ENDS **************************************************

graph = StateGraph(ChattingSchema)

########################### NODES ###############################
graph.add_node("chat_node", chat_node)



###########################3 EDGES ###########################
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# async def get_checpointer():
#     conn = await aiosqlite.connect("chatting_database.db", check_same_thread= False)
#     return AsyncSqliteSaver(conn=conn)
# checkpointer = get_checpointer()
workflow = graph
