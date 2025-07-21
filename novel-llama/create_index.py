from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Cấu hình Ollama
Settings.llm = Ollama(model="gemma3:1b", request_timeout=30.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# Đọc dữ liệu và tạo chỉ mục
documents = SimpleDirectoryReader('data').load_data()
index = VectorStoreIndex.from_documents(documents)

# Lưu chỉ mục
index.storage_context.persist(persist_dir="index_storage")