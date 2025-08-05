import streamlit as st
from langchain_openai import AzureChatOpenAI

st.title("🦜🔗 Azure OpenAI Quickstart App")

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

# Allow override from sidebar
st.sidebar.subheader("Azure OpenAI Settings (Optional)")
azure_openai_key = st.sidebar.text_input("Azure OpenAI API Key", value=secrets["AZURE_OPENAI_API_KEY"], type="password")
azure_endpoint = st.sidebar.text_input("Azure OpenAI Endpoint", value=secrets["AZURE_OPENAI_ENDPOINT"])
deployment_name = st.sidebar.text_input("Deployment Name", value=secrets["AZURE_OPENAI_DEPLOYMENT_NAME"])
api_version = st.sidebar.text_input("API Version", value=secrets["AZURE_OPENAI_API_VERSION"])

def generate_response(input_text):
    model = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        openai_api_key=azure_openai_key,
        openai_api_version=api_version,
        deployment_name=deployment_name,
        temperature=0.7
    )
    st.info(model.invoke(input_text))

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    
    if not all([azure_openai_key, azure_endpoint, deployment_name, api_version]):
        st.warning("Please fill in all Azure OpenAI settings in the sidebar!", icon="⚠")
    elif submitted:
        if not azure_openai_key or not azure_endpoint or not deployment_name:
            st.error("Please fill in all required Azure OpenAI settings!")
        else:
            with st.spinner('Generating response...'):
                try:
                    generate_response(text)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")