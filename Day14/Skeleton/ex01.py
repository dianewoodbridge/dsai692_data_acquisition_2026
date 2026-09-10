from dotenv import load_dotenv
import os

import streamlit as st
import google.generativeai as genai

load_dotenv()

model = genai.GenerativeModel("gemini-2.5-flash")
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
chat = model.start_chat()

st.set_page_config(page_title="Chatbot")
st.title("Interactive Chatbot with Google GenAI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages

# Save user message
