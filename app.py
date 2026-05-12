import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from agent import run_agent

st.title("🤖 AI Agent for Udit")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Ask anything:")

if user_input:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("Thinking..."):
        answer = run_agent(user_input, st.session_state.chat_history)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": str(answer)}
    )

    st.write(answer)