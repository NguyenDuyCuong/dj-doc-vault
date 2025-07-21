from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# Cấu hình Ollama
Settings.llm = Ollama(model="gemma3:1b", request_timeout=30.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# Tải chỉ mục
storage_context = StorageContext.from_defaults(persist_dir="index_storage")
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