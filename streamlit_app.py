import os
from os.path import join, dirname
from dotenv import load_dotenv

import streamlit as st

import openai
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")

documents = SimpleDirectoryReader("files").load_data()
index = GPTVectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

with st.sidebar:
    "[株式会社マネーフォワード-決算説明資料](https://corp.moneyforward.com/ir/library/presentation/)"

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "マネーフォワードの2023年11月期の決算情報について回答できます"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = query_engine.query(prompt)
    msg = response.response
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg)
