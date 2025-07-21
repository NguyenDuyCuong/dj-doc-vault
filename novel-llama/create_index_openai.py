import os
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings


# Lấy thông tin nhạy cảm từ biến môi trường
api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
embed_api_key = os.getenv("AZURE_OPENAI_EMBED_API_KEY", api_key)
embed_endpoint = os.getenv("AZURE_OPENAI_EMBED_ENDPOINT")

llm = AzureOpenAI(
    model="DeepSeek-R1-0528",
    deployment_name="DeepSeek-R1-0528",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version="2024-05-01-preview",
    reuse_client=False
)

embed_model = AzureOpenAIEmbedding(
    model="text-embedding-3-small",
    deployment_name="text-embedding-3-small",
    api_key=embed_api_key,
    azure_endpoint=embed_endpoint,
    api_version="2023-05-15",
    reuse_client=False
)

Settings.llm = llm
Settings.embed_model = embed_model

documents = SimpleDirectoryReader('data').load_data()
# Tạo index từ dữ liệu
index = VectorStoreIndex.from_documents(documents)

# Lưu index ra file
index.storage_context.persist(persist_dir="index_storage_openai")

print("Index đã được tạo và lưu tại 'index_storage_openai'")