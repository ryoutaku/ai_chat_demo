import os
from os.path import join, dirname
from dotenv import load_dotenv
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
import openai

# OpenAIのAPIkey読み込み
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# LlamaIndexのインデックス作成
documents = SimpleDirectoryReader("files").load_data()
index = GPTVectorStoreIndex.from_documents(documents)

# LlamaIndexのインデックス保存
context = index.storage_context
context.persist(persist_dir="./storage_context")