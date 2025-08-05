import streamlit as st
from openai import AzureOpenAI

# Azure OpenAI settings from secrets
DEFAULT_CONFIG = {
    "AZURE_OPENAI_API_KEY": "",
    "AZURE_OPENAI_ENDPOINT": "https://your-resource-name.openai.azure.com",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "your-deployment-name",
    "AZURE_OPENAI_API_VERSION": "2024-05-01-preview"
}

# Load secrets with defaults
secrets = {}
for key, default in DEFAULT_CONFIG.items():
    secrets[key] = st.secrets.get(key, default)

with st.sidebar:
    st.subheader("Azure OpenAI Settings")
    azure_openai_key = st.text_input("Azure OpenAI API Key", 
                                  value=secrets["AZURE_OPENAI_API_KEY"], 
                                  type="password")
    azure_endpoint = st.text_input("Azure OpenAI Endpoint",
                                 value=secrets["AZURE_OPENAI_ENDPOINT"])
    deployment_name = st.text_input("Deployment Name",
                                  value=secrets["AZURE_OPENAI_DEPLOYMENT_NAME"])
    api_version = st.text_input("API Version",
                              value=secrets["AZURE_OPENAI_API_VERSION"])

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not all([azure_openai_key, azure_endpoint, deployment_name]):
        st.error("Please provide all required Azure OpenAI settings in the sidebar.")
        st.stop()

    try:
        client = AzureOpenAI(
            api_key=azure_openai_key,
            api_version=api_version,
            azure_endpoint=azure_endpoint
        )
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        response = client.chat.completions.create(
            model=deployment_name,
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.stop()
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
