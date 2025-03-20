import streamlit as st
from io import StringIO

# Configure Streamlit page
st.set_page_config(page_title="Chatbot", layout="wide")

# Custom CSS for a ChatGPT/Copilot-like professional look
st.markdown("""
    <style>
    /* Overall page styling */
    body {
        background-color: #f4f4f5;
        margin: 0;
        padding: 0;
    }

    /* Chat container */
    .chat-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        max-width: 800px;
        margin: 20px auto;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        min-height: 70vh;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 1px solid #e5e7eb;
    }

    /* Title styling */
    .title {
        font-family: 'Times New Roman', Times, serif;
        font-size: 32px;
        font-weight: bold;
        color: #1f2937;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Message container to handle dynamic height */
    .message-container {
        flex-grow: 1;
        overflow-y: auto;
        padding-bottom: 20px;
    }

    /* Message styles */
    .chat-message {
        padding: 12px 16px;
        margin: 10px 0;
        border-radius: 8px;
        max-width: 80%;
        word-wrap: break-word;
        line-height: 1.5;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 16px;
    }

    /* User message */
    .user-message {
        background-color: #e1f5fe;
        color: #1e3a8a;
        margin-left: auto;
        text-align: right;
    }

    /* Bot message */
    .bot-message {
        background-color: #f3f4f6;
        color: #1f2937;
        margin-right: auto;
        text-align: left;
    }

    /* Input container */
    .input-container {
        display: flex;
        gap: 10px;
        padding: 10px 0;
        background-color: #ffffff;
        border-top: 1px solid #e5e7eb;
    }

    /* Input field */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        padding: 12px 16px !important;
        border: 1px solid #d1d5db !important;
        font-size: 16px !important;
        background-color: #f9fafb !important;
        min-height: 48px !important;
        flex-grow: 1;
    }

    .stTextInput > div > div > input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 5px rgba(59,130,246,0.3) !important;
    }

    /* Button */
    .stButton > button {
        border-radius: 8px !important;
        background-color: #3b82f6 !important;
        color: white !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        border: none !important;
        min-height: 48px !important;
    }

    .stButton > button:hover {
        background-color: #2563eb !important;
    }

    /* Settings container */
    .settings-container {
        background-color: #f9fafb;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        border: 1px solid #e5e7eb;
    }

    /* File uploader */
    .uploadedFile {
        border: 1px dashed #d1d5db;
        border-radius: 8px;
        padding: 10px;
        background-color: #ffffff;
    }

    .uploadedFile:hover {
        border-color: #3b82f6;
        background-color: #f0f9ff;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Predefined chatbot responses (over 30)
def get_bot_response(user_input, file_content=""):
    user_input = user_input.lower().strip()
    responses = {
        "hello": "Hey there! What’s up?",
        "hi": "Hi! How can I help you today?",
        "hey": "Hey! What’s on your mind?",
        "how are you": "I’m good, thanks! How about you?",
        "good morning": "Good morning! How’s your day starting?",
        "good night": "Good night! Sleep well!",
        "bye": "See you later! Take care!",
        "thanks": "You’re welcome! Anything else?",
        "thank you": "No problem! What’s next?",
        "what’s your name": "I’m your friendly Chatbot! What’s yours?",
        "who are you": "I’m a simple bot here to chat with you!",
        "what can you do": "I can answer questions, chat, or summarize files!",
        "how’s the weather": "I’d say sunny, but I’m indoors—how’s it where you are?",
        "tell me a joke": "Why don’t skeletons fight? They don’t have guts!",
        "what time is it": "Check your clock—I’m timeless!",
        "where are you": "Right here in your browser!",
        "what’s new": "Not much, just chatting with cool people like you!",
        "i’m bored": "Let’s chat then—what’s your favorite hobby?",
        "help": "Sure, what do you need help with?",
        "tell me something": "Did you know octopuses have three hearts?",
        "who made you": "Some clever folks coded me up!",
        "are you real": "As real as a digital buddy can be!",
        "what’s your favorite color": "I like blue—matches my vibe!",
        "how old are you": "I’m ageless—born today, every day!",
        "do you sleep": "Nope, I’m always awake for you!",
        "what’s for dinner": "How about pizza? What do you like?",
        "i’m hungry": "Grab a snack—what’s your favorite food?",
        "tell me a story": "Once upon a time, a bot helped a user… that’s us now!",
        "why": "Why not? Life’s full of questions!",
        "yes": "Cool, what’s next?",
        "no": "Alright, anything else on your mind?",
        "okay": "Sweet! What else you got?",
        "nice": "Glad you think so! What’s up?",
        "haha": "Funny, right? What made you laugh?"
    }

    # Default response
    default_response = "Hmm, I don’t know that one. Try something else!"

    # File-based response
    if file_content:
        return f"From your file: '{file_content[:50]}...' — anything specific you want to talk about?"

    return responses.get(user_input, default_response)

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main app layout
st.markdown('<div class="title">🤖 Chatbot Buddy</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Message container
st.markdown('<div class="message-container">', unsafe_allow_html=True)

# Settings section
with st.expander("Settings", expanded=False):
    st.markdown('<div class="settings-container">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])
    st.markdown('</div>', unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="chat-message user-message">{message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input section
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Say something...", key="user_input", placeholder="Type here...", label_visibility="collapsed")
    with col2:
        send_button = st.button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Process input and generate response
if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    context = StringIO(uploaded_file.getvalue().decode("utf-8")).read() if uploaded_file else ""
    bot_response = get_bot_response(user_input, context)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)