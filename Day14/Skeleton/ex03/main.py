import streamlit as st

job_posting_page = st.Page(
    "job_posting.py", title="Table View", icon=":material/table:")
chat_bot_page = st.Page(
    "chatbot.py", title="Chatbot", icon=":material/chat:")

pg = st.navigation([job_posting_page, chat_bot_page])
st.set_page_config(page_title="Career Dashboard",
                   page_icon=":material/interactive_space:")
pg.run()
