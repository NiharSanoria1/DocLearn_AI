"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from DocLearn_AI import style
from DocLearn_AI.reflex_state import State
from rxconfig import config

# sidebar
def sidebar()-> rx.Component:
        return rx.box(
            rx.vstack(
                rx.heading("Chats", size="4", color="gray"),
                rx.button("+ New Chat", width="100%", variant="surface"),
                rx.divider(),
                #placeholder for history items
                rx.text("Previous chat 1", color="gray"),
                rx.text("Previous chat 2", color="gray"),
                spacing="4",
                padding="1em"
            ),
            width="260px",
            height="100vh",
            background_color = "#f5f5f534",
            border_right="1px solid #e0e0e0",
            display=["none", "none", "block"], # Hide on mobile, show on desktop
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
            width="100%"
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



# rx.center(
#        rx.vstack(
#            chat(),
#           action_bar(),
#            align="stretch"
#        )
#    )


app = rx.App()
app.add_page(index)
