
import reflex as rx
from DocLearn_AI import style
from DocLearn_AI.reflex_state import State
from rxconfig import config



# sidebar item component 
def sidebar_item(chat_session: dict) -> rx.Component:
    """A single button representing a chat session"""

    return rx.hstack(
        rx.button(
            rx.icon("message-square", size = 16),
            rx.text(chat_session["title"], size="1", truncate=True), # truncate uuid so it fits
            # layout property
            variant = "ghost",
            width="100%",

            style={
                "justify_content": "flex-start",
                "padding_left": "1em"
            },

            #functionality
            color_scheme= "gray",
            on_click= State.select_chat(chat_session["id"]),
        ),
        #actions (edit/delete)
        rx.hstack(
            # edit button
            rx.icon_button(
                rx.icon("pencil", size =14),
                variant="ghost",
                size="1",
                on_click=State.start_renaming(chat_session["id"], chat_session["title"])
            ),
            rx.icon_button(
                rx.icon("trash-2", size= 14),
                variant= "ghost",
                size="1",
                color_scheme="ruby",
                on_click=State.delete_chat(chat_session["id"])
            ),
            spacing="1",
        ),
        
        width = "100%",
        align_items="center",
        padding_right="0.5em",
        # highlight if active
        background_color= rx.cond(
            State.thread_id == chat_session["id"],
            "#80555512",
            "transparent"
        ), 
        border_radius = "6px"
    )
    
#---------rename dialog------------
def rename_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Rename Chat"),
            rx.dialog.description("Enter a new name for this chat."),
            rx.vstack(
                rx.input(
                    placeholder="New Title",
                    value= State.new_chat_title,
                    on_change=State.set_new_chat_title
                ),
                rx.hstack(
                    rx.button("Cancel", variant="soft", color_scheme="gray", on_click=State.cancel_renaming),
                    rx.button("Save", on_click=State.save_chat_title),
                    spacing="3",
                    justify="end",
                    width="100%"
                ),
                spacing="4",
                margin_top = "1em"
            ),
            max_width = "400px",
        ),
        open=State.is_renaming,
        on_open_change=State.set_is_renaming
    )
    
# sidebar
def sidebar()-> rx.Component:
        return rx.box(
            rx.vstack(
                rx.heading("Chats", size="4", color = "gray"),
                
                # new chat button
                rx.button(
                    "+ New Chat",
                    width= "100%",
                    variant = "surface",
                    on_click=State.create_new_chat
                ),
                
                rx.divider(),
                
                #dynamic chat list
                
                rx.vstack(
                    rx.foreach(
                        State.chat_sessions,
                        sidebar_item
                    ),
                    width="100%",
                    spacing="1",
                    overflow_y="auto", # allow scroling sidebar if many chats
                    flex ="1",
                    align_items="stretch",
                    
                ),
                spacing="4",
                padding="1em",
                height= "100%"
            ),
            width = "260px",
            height="100vh",
            background_color= "#f9f9f909",
            border_right="1px solid #e0e0e0",
            display = ["none", "none", "block"]
        )
    
    
    
    
    

# question answer function
def qa(question : str, answer: str) -> rx.Component:
    return rx.box(
        rx.box( 
               rx.text(question, style=style.question_style),
               text_align = "right", 
               margin_top="1em")
            ,
        rx.box(
            rx.text(answer, style=style.answer_style),
            text_align = "left", 
            margin_top="0.5em")
            ,
        width="100%",
    )

# chatting function    
def chat() -> rx.Component:
    
    return rx.vstack(
        rx.foreach(
            State.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        ),
        rx.box(id="chat-end"),
        width="100%",
        spacing="2",
        padding_bottom="2em"
    )

    
    
# input funtionality
def action_bar() -> rx.Component:
    return rx.hstack(
        rx.input(
            value = State.question,
            placeholder="type your question here", 
            on_change=State.set_question,
            style= style.input_style,
            width="100%",
            on_key_down=State.check_enter_key,
            
            id="question_input"
            ),
        
        rx.button("ask", 
               # alling the answer function
               on_click=State.answer,
               style=style.button_style
               ),
        width="100%",
        padding="1em",
        # background_color = "white",
        # border_top="1px solid #e0e0e0"
        max_width="800px",
        margin_x="auto"
    )

def index() -> rx.Component:
   return rx.hstack(
       # left sidebar
       sidebar(),
       rename_dialog(),
       # right, main chat area
       
       rx.vstack(
           #chat history
           rx.box(
               rx.container(
                   chat(),
                   size="3"
               ),
               width="100%",
               height="100%",
               overflow_y="auto",
               flex="1",
               padding_top="2em"
            ),
           rx.box(
               action_bar(),
               width="100%",
               padding_bottom="1em"
           ),
           height="100vh",
           width="100%",
           spacing="0"
        ),
       spacing="0"
    )

app = rx.App()
app.add_page(index, on_load=State.fetch_chat_sessions)
