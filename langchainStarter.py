import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage

#LangSmith Link: https://smith.langchain.com/o/7c217141-8f24-47fb-9453-8636ac7795fe/projects/p/84230bef-e7ae-4404-9e2c-eae850709c17?timeModel=%7B%22duration%22%3A%227d%22%7D 

# Load environment variables
load_dotenv()

# Access API keys
GPTapi_key = os.getenv("OPENAI_API_KEY")
ANTapi_key = os.getenv("ANTHROPIC_API_KEY")

# Validate API keys
if not GPTapi_key or not ANTapi_key:
    st.error("API keys are missing. Please check your .env file.")

# Streamlit app title and sidebar
st.title("AI Chat Starter")
st.sidebar.header("Settings")

# Model selection
model_choice = st.sidebar.selectbox("Choose AI Model", ["OpenAI GPT-3.5", "Anthropic Claude"])

# Initialize the model based on the selection
if model_choice == "OpenAI GPT-3.5":
    model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=GPTapi_key)
elif model_choice == "Anthropic Claude":
    model = ChatAnthropic(model_name="claude-2.1", anthropic_api_key=ANTapi_key)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.text_input("Enter your message:")

# Submit button
if st.button("Send"):
    if user_input:
        # Append user message to chat history
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        
        # Get model response
        try:
            response = model(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=response.content))
        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history
st.subheader("Chat History")
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        st.write(f"**You:** {message.content}")
    elif isinstance(message, AIMessage):
        st.write(f"**{model_choice}:** {message.content}")

# Clear chat history
if st.button("Clear Chat"):
    st.session_state.chat_history = []
    st.info("Chat history cleared!")
