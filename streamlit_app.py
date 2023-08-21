import os
from os.path import join, dirname
from dotenv import load_dotenv

import streamlit as st

import openai
from llama_index import StorageContext, ServiceContext, load_index_from_storage
from llama_index.callbacks import CallbackManager, LlamaDebugHandler
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
from llama_index.vector_stores import SimpleVectorStore

# OpenAIのAPIkey読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# LlamaIndexのインデックス読み込み
storage_context = StorageContext.from_defaults(
    docstore=SimpleDocumentStore.from_persist_dir(persist_dir="./storage_context"),
    vector_store=SimpleVectorStore.from_persist_dir(persist_dir="./storage_context"),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir="./storage_context"),
)
llama_debug_handler = LlamaDebugHandler()
callback_manager = CallbackManager([llama_debug_handler])
service_context = ServiceContext.from_defaults(callback_manager=callback_manager)
index = load_index_from_storage(storage_context, service_context=service_context)
query_engine = index.as_query_engine()

# チャット画面の実装
with st.sidebar:
    "[株式会社マネーフォワード-決算説明資料](https://corp.moneyforward.com/ir/library/presentation/)"
    "【質問例】"
    "マネーフォワードの法人向けサービスは何があるか。"
    "法人向けARPAについて、SMBセグメントはQoQでフラットなのか。"
    "中堅企業及び中小企業のARPAと顧客数のYoY成長率、またはQoQの成長率を教えていただきたい。"

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "マネーフォワードの2023年11月期の決算情報について回答できます"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = query_engine.query(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response.response})
    st.chat_message("assistant").write(response.response)
