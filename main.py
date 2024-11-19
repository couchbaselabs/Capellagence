import streamlit as st
import json
import time

import html
import re

assistant_avatar_url = "https://raw.githubusercontent.com/couchbaselabs/Capellagence/refs/heads/master/capellagence.png"
user_avatar_url = "https://www.w3schools.com/w3images/avatar2.png"
couchbase_logo = "https://emoji.slack-edge.com/T024FJS4M/couchbase/4a361e948b15ed91.png"

# Custom CSS for sticky header and chat container
st.markdown(f"""
<style>
/* Sticky header */
.header {{
    position: fixed;
    height: 55px;
    top: 5px;
    width: 100%;
    z-index: 9999999;
    display: flex;
    align-items: center;
    padding: 10px;
}}


/* Hide the Streamlit header and footer */
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}

</style>
""", unsafe_allow_html=True)


def display_message(text, is_user=False, avatar_url=None):
    """Displays a chat message with custom styling and avatar."""
    avatar_style = "width:40px; height:40px; margin:0;"
    message_bg_color = (
        "linear-gradient(135deg, #00B2FF 0%, #006AFF 100%)" if is_user else "#71797E"
    )
    alignment = "flex-end" if is_user else "flex-start"
    margin = "margin-left" if is_user else "margin-right"

    formatted_text = text.strip()

    if is_user:
        container_html = f"""
        <div style="display:flex; align-items:flex-start; justify-content:{alignment}; margin-bottom:10px;">
            <div style="background:{message_bg_color}; color:white; border-radius:20px; padding:10px; {margin}:5px; max-width:90%; font-size:14px; line-height:1.2; word-wrap:break-word;">
                {formatted_text}
            </div>
        </div>
        """
    else:
        current_time = time.strftime("%H:%M", time.localtime())
        container_html = f"""
        <div style="display:flex; align-items:flex-start; justify-content:{alignment}; margin-bottom:10px;">
            <img src="{avatar_url}" alt="avatar" style="{avatar_style}; margin-right:5px;" />
            <div style="background:{message_bg_color}; color:white; border-radius:20px; padding:10px; max-width:90%; font-size:14px; line-height:1.2; word-wrap:break-word;">
                {formatted_text}
                <div style="font-size:12px; color:#ccc; margin-top:5px;">{current_time}</div>
            </div>
        </div>
        """
    st.write(container_html, unsafe_allow_html=True)

def normalize_text(text):
    text = re.sub(r'(?<!\s)\n(?!\s)', ' ', text)
    return text.lower().strip()

# Load predefined responses from a config file
def load_responses():
    with open('responses.json', 'r') as file:
        return json.load(file)

# Initialize responses
responses = load_responses()

# Display the title with the Couchbase logo
st.markdown(f"""
<div class="header">
    <img src="{couchbase_logo}" alt="Couchbase Logo" style="width:40px; height:40px; margin-right:10px;" />
    <h1 style="margin:0;">Capellagence</h1>
</div>
""", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = []

display_message("Hello! How can I assist you today?", is_user=False, avatar_url=assistant_avatar_url)

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        display_message(message["content"], is_user=True)
    else:
        display_message(message["content"], is_user=False, avatar_url=assistant_avatar_url)

# User input
if question := st.chat_input("Ask a question"):
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": question})
    # Display user message
    display_message(question, is_user=True)

    # Display "Thinking..." message using a placeholder
    thinking_placeholder = st.empty()
    thinking_message = "Thinking..."
    thinking_avatar_url = assistant_avatar_url
    # Display the "Thinking..." message
    with thinking_placeholder.container():
        display_message(thinking_message, is_user=False, avatar_url=thinking_avatar_url)

    # Get response from predefined responses
    normalized_question = normalize_text(question)
    response = None
    for key in responses:
      if normalize_text(key) == normalized_question:
          response = responses[key]
          break
    if response is None:
      response = "I'm not sure how to respond to that."

    # Calculate delay duration based on response length
    # For example, 0.05 seconds per character
    delay_duration = len(response) * 0.005
    time.sleep(delay_duration)

    # Clear the "Thinking..." message
    thinking_placeholder.empty()

    # Append assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": response})
    # Display assistant message
    display_message(response, is_user=False, avatar_url=assistant_avatar_url)