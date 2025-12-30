import os
import streamlit as st
from langchain_openai import ChatOpenAI
from openaiapikey import openai_key

# Set API key
os.environ["OPENAI_API_KEY"] = openai_key

st.title("LangChain Demo with OpenAI")

input_text = st.text_input("Search the topic you want")

# OpenAI LLM (chat-based)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.8
)

if input_text:
    response = llm.invoke(input_text)
    st.write(response.content)