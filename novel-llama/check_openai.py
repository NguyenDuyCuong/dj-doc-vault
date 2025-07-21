import os
from openai import AzureOpenAI

# Lấy thông tin nhạy cảm từ biến môi trường
api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
embed_api_key = os.getenv("AZURE_OPENAI_EMBED_API_KEY", api_key)
embed_endpoint = os.getenv("AZURE_OPENAI_EMBED_ENDPOINT")

client = AzureOpenAI(
    api_key=api_key,
    api_version="2025-01-01-preview",
    azure_endpoint=azure_endpoint
)

completion = client.chat.completions.create(
    model="o4-mini", # Replace with your model deployment name.
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "When was Microsoft founded?"}
    ],
    stream=True
)

for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end='')

# Tạo client cho embedding
client1 = AzureOpenAI(
    api_key=embed_api_key,
    api_version="2023-05-15",
    azure_endpoint=embed_endpoint
)

embedding = client1.embeddings.create(
    model="text-embedding-3-small", # Replace with your model deployment name
    input="Attenion is all you need",
    encoding_format="float"
)

print(embedding)
