import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(page_title="Groq Chatbot", page_icon="🤖")
st.title("🤖 Groq Chatbot")

# Fail early if the API key is missing (ChatGroq reads GROQ_API_KEY from env)
if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY is not set. Add it to your .env file and restart.")
    st.stop()


@st.cache_resource
def get_model() -> ChatGroq:
    # Created once and reused across reruns
    return ChatGroq(model="openai/gpt-oss-120b")


model = get_model()

# Streamlit reruns the script on every interaction, so history lives in session_state
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# Sidebar
with st.sidebar:
    st.header("Options")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.rerun()

# Render past messages (skip the system message)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)

# Handle new input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Stream tokens as they arrive
            reply = st.write_stream(
                chunk.content for chunk in model.stream(st.session_state.messages)
            )
            st.session_state.messages.append(AIMessage(content=reply))
        except Exception as e:
            # Roll back the unanswered user message so history stays consistent
            st.session_state.messages.pop()
            st.error(f"Request failed: {e}")