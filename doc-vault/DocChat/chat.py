"""Utility for calling Azure OpenAI with the new openai >=1.0 client.
Read credentials from environment variables that were loaded via python-dotenv.
"""
import os
from openai import AzureOpenAI

# Initialise client once at import time so it's reused across requests
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def chat_completion(messages: list[dict]) -> str:
    """Send a chat completion request and return the assistant message text."""
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_MODEL"),
        messages=messages,
        temperature=0.7,
    )
    return response.choices[0].message.content