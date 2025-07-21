
import os
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings


# Lấy thông tin nhạy cảm từ biến môi trường
api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
embed_api_key = os.getenv("AZURE_OPENAI_EMBED_API_KEY", api_key)
embed_endpoint = os.getenv("AZURE_OPENAI_EMBED_ENDPOINT")

llm = AzureOpenAI(
    model="o4-mini",
    deployment_name="o4-mini",
    api_key=api_key,
    azure_endpoint=azure_endpoint,
    api_version="2025-01-01-preview",
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

# Tải chỉ mục
storage_context = StorageContext.from_defaults(persist_dir="index_storage_openai")
index = load_index_from_storage(storage_context)

# Tạo query engine
query_engine = index.as_query_engine()

# Vòng lặp tương tác để hỏi liên tục
while True:
    user_input = input("Nhập câu hỏi (hoặc 'exit' để thoát): ")
    if user_input.lower() == 'exit':
        break
    try:
        response = query_engine.query(user_input)
        print("Trả lời:", response)
    except Exception as e:
        print("Đã xảy ra lỗi khi truy vấn:", str(e))