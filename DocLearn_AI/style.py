# style.py
import reflex as rx

# Common styles for questions and answers.
shadow = "0 4px 6px -1px rgba(0, 0, 0, 0.3)" # Darker, smoother shadow
chat_margin = "20%"

message_style = dict(
    padding="1.25em",       # More breathing room
    border_radius="12px",   # Softer, modern corners
    margin_y="0.5em",
    box_shadow=shadow,
    max_width="800px",      # Increased from 30em to fit code/markdown better
    display="inline-block",
)

# Set specific styles for questions and answers.
question_style = message_style | dict(
    margin_left=chat_margin,
    background_color=rx.color("gray", 4), # Standard gray for user
    color="white",
)

answer_style = message_style | dict(
    margin_right=chat_margin,
    
    # --- DARK THEME FIX ---
    background_color="#262626",  # Soft Dark Charcoal (Pleasant on eyes)
    color="#E5E5E5",             # Off-white Text (Reduces eye strain)
    border="1px solid #333333",  # Subtle border for definition
)

# Styles for the action bar.
input_style = dict(
    border_width="1px",
    padding="0.5em",
    box_shadow=shadow,
    width="100%", # Changed to 100% to fill the broad container
)

button_style = dict(
    background_color=rx.color("accent", 10),
    box_shadow=shadow,
)