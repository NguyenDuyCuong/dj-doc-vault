import streamlit as st
from openai import AzureOpenAI
from typing import List, Dict, Any, Union, Optional, Tuple
import os
import json
import shutil
import uuid
from datetime import datetime
from pathlib import Path
import base64
from dataclasses import dataclass, asdict, field
from enum import Enum

class DocumentType(Enum):
    TEXT = "text"
    PDF = "pdf"
    IMAGE = "image"
    OTHER = "other"

@dataclass
class DocumentVersion:
    version_id: str
    timestamp: str
    size: int
    path: str

@dataclass
class DocumentMetadata:
    doc_id: str
    name: str
    doc_type: DocumentType
    created_at: str
    updated_at: str
    folder: str = ""
    tags: List[str] = field(default_factory=list)
    versions: List[DocumentVersion] = field(default_factory=list)
    is_archived: bool = False
    description: str = ""

class DocumentManager:
    def __init__(self, base_dir: str = "uploaded_docs"):
        self.base_dir = Path(base_dir)
        self.metadata_file = self.base_dir / "metadata.json"
        self.metadata: Dict[str, DocumentMetadata] = {}
        self._ensure_directories()
        self._load_metadata()
    
    def _ensure_directories(self):
        """Ensure all required directories exist."""
        self.base_dir.mkdir(exist_ok=True, parents=True)
        (self.base_dir / "versions").mkdir(exist_ok=True)
    
    def _load_metadata(self):
        """Load metadata from disk."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.metadata = {k: self._dict_to_metadata(v) for k, v in data.items()}
            except Exception as e:
                st.error(f"Error loading metadata: {str(e)}")
                self.metadata = {}
    
    def _save_metadata(self):
        """Save metadata to disk."""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump({k: asdict(v) for k, v in self.metadata.items()}, f, indent=2)
    
    def _dict_to_metadata(self, data: dict) -> DocumentMetadata:
        """Convert dictionary to DocumentMetadata object."""
        versions = [
            DocumentVersion(**v) if isinstance(v, dict) else v 
            for v in data.get('versions', [])
        ]
        data['versions'] = versions
        data['doc_type'] = DocumentType(data['doc_type'])
        return DocumentMetadata(**data)
    
    def _get_doc_type(self, filename: str) -> DocumentType:
        """Determine document type from filename."""
        ext = Path(filename).suffix.lower()
        if ext in ['.txt', '.md', '.csv', '.json']:
            return DocumentType.TEXT
        elif ext == '.pdf':
            return DocumentType.PDF
        elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return DocumentType.IMAGE
        return DocumentType.OTHER
    
    def add_document(self, file, folder: str = "", tags: List[str] = None, 
                    description: str = "") -> Tuple[bool, str]:
        """Add a new document with versioning support."""
        try:
            content = file.read()
            filename = file.name
            doc_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            # Create document directory
            doc_dir = self.base_dir / doc_id
            doc_dir.mkdir(exist_ok=True)
            
            # Save file
            filepath = doc_dir / filename
            filepath.write_bytes(content)
            
            # Create version
            version_id = str(uuid.uuid4())
            version_path = self.base_dir / "versions" / f"{doc_id}_{version_id}"
            shutil.copy2(filepath, version_path)
            
            # Create metadata
            doc_metadata = DocumentMetadata(
                doc_id=doc_id,
                name=filename,
                doc_type=self._get_doc_type(filename),
                created_at=now,
                updated_at=now,
                folder=folder,
                tags=tags or [],
                versions=[
                    DocumentVersion(
                        version_id=version_id,
                        timestamp=now,
                        size=len(content),
                        path=str(version_path.relative_to(self.base_dir))
                    )
                ],
                description=description
            )
            
            self.metadata[doc_id] = doc_metadata
            self._save_metadata()
            return True, doc_id
            
        except Exception as e:
            return False, str(e)
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document and all its versions."""
        if doc_id not in self.metadata:
            return False
            
        try:
            # Remove document directory
            doc_dir = self.base_dir / doc_id
            if doc_dir.exists():
                shutil.rmtree(doc_dir)
            
            # Remove all versions
            for version in self.metadata[doc_id].versions:
                version_path = self.base_dir / version.path
                if version_path.exists():
                    version_path.unlink()
            
            # Remove from metadata
            del self.metadata[doc_id]
            self._save_metadata()
            return True
            
        except Exception as e:
            st.error(f"Error deleting document: {str(e)}")
            return False
    
    def search_documents(self, query: str, search_content: bool = False) -> List[DocumentMetadata]:
        """Search documents by name, tags, or content."""
        query = query.lower()
        results = []
        
        for doc in self.metadata.values():
            # Search in name
            if query in doc.name.lower():
                results.append(doc)
                continue
                
            # Search in tags
            if any(query in tag.lower() for tag in doc.tags):
                results.append(doc)
                continue
                
            # Search in content (for text files)
            if search_content and doc.doc_type == DocumentType.TEXT:
                try:
                    doc_path = self.base_dir / doc.doc_id / doc.name
                    if doc_path.exists():
                        content = doc_path.read_text(encoding='utf-8').lower()
                        if query in content:
                            results.append(doc)
                except:
                    continue
        
        return results
    
    def get_document_path(self, doc_id: str) -> Optional[Path]:
        """Get the path to a document."""
        if doc_id not in self.metadata:
            return None
        doc = self.metadata[doc_id]
        return self.base_dir / doc_id / doc.name
    
    def get_document_content(self, doc_id: str) -> Optional[Union[str, bytes]]:
        """Get document content."""
        doc_path = self.get_document_path(doc_id)
        if not doc_path or not doc_path.exists():
            return None
            
        try:
            doc = self.metadata[doc_id]
            if doc.doc_type == DocumentType.TEXT:
                return doc_path.read_text(encoding='utf-8')
            else:
                return doc_path.read_bytes()
        except Exception as e:
            st.error(f"Error reading document: {str(e)}")
            return None

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

# Initialize document manager
doc_manager = DocumentManager()

def render_document_manager_ui():
    """Render the document management UI."""
    st.sidebar.subheader("Document Manager")
    
    # Search documents
    search_query = st.sidebar.text_input("Search documents")
    if search_query:
        results = doc_manager.search_documents(search_query, search_content=True)
        st.sidebar.write(f"Found {len(results)} documents matching '{search_query}'")
    
    # Upload section
    with st.sidebar.expander("📤 Upload Documents", expanded=True):
        uploaded_files = st.file_uploader("Choose files", 
                                        type=("txt", "md", "pdf", "jpg", "jpeg", "png"),
                                        accept_multiple_files=True,
                                        key="doc_uploader")
        
        if uploaded_files:
            folder = st.text_input("Folder (optional)")
            tags = st.text_input("Tags (comma-separated)", "")
            description = st.text_area("Description (optional)", "")
            
            if st.button("Upload"):
                for file in uploaded_files:
                    success, doc_id = doc_manager.add_document(
                        file, 
                        folder=folder,
                        tags=[t.strip() for t in tags.split(",") if t.strip()],
                        description=description
                    )
                    if success:
                        st.success(f"Uploaded {file.name}")
                    else:
                        st.error(f"Failed to upload {file.name}")
    
    # Document list
    st.sidebar.subheader("Documents")
    
    # Group by folder
    folders = {}
    for doc in doc_manager.metadata.values():
        folder_name = doc.folder or "Uncategorized"
        if folder_name not in folders:
            folders[folder_name] = []
        folders[folder_name].append(doc)
    
    for folder_name, docs in folders.items():
        with st.sidebar.expander(f"📁 {folder_name} ({len(docs)})", expanded=True):
            for doc in sorted(docs, key=lambda x: x.updated_at, reverse=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{doc.name}**")
                    if doc.description:
                        st.caption(doc.description)
                    if doc.tags:
                        st.caption(", ".join(f"#{t}" for t in doc.tags))
                with col2:
                    if st.button("🗑️", key=f"del_{doc.doc_id}"):
                        if doc_manager.delete_document(doc.doc_id):
                            st.rerun()
                
                # Show document preview/actions
                with st.expander("View/Manage"):
                    st.write(f"**Type:** {doc.doc_type.value}")
                    st.write(f"**Uploaded:** {doc.created_at}")
                    st.write(f"**Versions:** {len(doc.versions)}")
                    
                    # Version management
                    if st.button("Upload New Version", key=f"version_{doc.doc_id}"):
                        new_version = st.file_uploader("Upload new version", 
                                                     type=Path(doc.name).suffix[1:],
                                                     key=f"version_upload_{doc.doc_id}")
                        if new_version:
                            # Add as new version
                            success, _ = doc_manager.add_document(
                                new_version,
                                folder=doc.folder,
                                tags=doc.tags,
                                description=doc.description
                            )
                            if success:
                                st.success("New version uploaded")
                                st.rerun()
                    
                    # Document preview
                    if st.button("Preview", key=f"preview_{doc.doc_id}"):
                        content = doc_manager.get_document_content(doc.doc_id)
                        if content is not None:
                            if doc.doc_type == DocumentType.TEXT:
                                st.text_area("Document Content", content, height=200)
                            else:
                                st.image(content, caption=doc.name)

# Initialize the document manager UI
doc_manager = DocumentManager()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_docs" not in st.session_state:
    st.session_state.selected_docs = set()

# Initialize document manager and render UI
render_document_manager_ui()

with st.sidebar:
    st.subheader("Document Manager")
    
    # Document upload section
    uploaded_files = st.file_uploader("Upload documents", 
                                    type=("txt", "md", "pdf", "jpg", "png"), 
                                    key="file_uploader",
                                    accept_multiple_files=True)
    
    st.markdown("---")
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

# Document selection and chat interface
st.title("📝 Document Chat with Azure OpenAI")

# Check if we have documents
if not doc_manager.metadata:
    st.info("Please upload some documents using the sidebar to get started.")
    st.stop()

# Display selected documents
if st.session_state.selected_docs:
    selected_docs = [doc_manager.metadata[doc_id] for doc_id in st.session_state.selected_docs]
    doc_names = ", ".join(doc.name for doc in selected_docs)
    st.info(f"Active documents: {doc_names}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Document selection
if not st.session_state.selected_docs:
    st.warning("Please select documents to chat with from the sidebar.")

# Chat input
if prompt := st.chat_input("Ask me about the document..."):
    if not all([azure_openai_key, azure_endpoint, deployment_name]):
        st.error("Please provide all required Azure OpenAI settings in the sidebar.")
        st.stop()
    
    if not st.session_state.selected_docs:
        st.error("Please select at least one document to chat with.")
        st.stop()
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Initialize Azure OpenAI client
            client = AzureOpenAI(
                api_key=azure_openai_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint
            )
            
            # Prepare the conversation history
            messages = [
                {"role": "system", "content": """You are a helpful assistant that answers questions about the provided document. 
                 Use the following document content to answer questions. If the answer isn't in the document, say so.\n\n"""}
            ]
            
                        # Add selected documents to system message
            messages[0]["content"] += "Document contents:\n\n"
            for doc_id in st.session_state.selected_docs:
                doc = doc_manager.metadata[doc_id]
                content = doc_manager.get_document_content(doc_id)
                if content is not None:
                    if isinstance(content, bytes):
                        content = f"[Binary file: {doc.name}, size: {len(content)} bytes]"
                    messages[0]["content"] += f"--- {doc.name} ---\n{content}\n\n"
            
            # Add conversation history
            for msg in st.session_state.messages:
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Get the response from Azure OpenAI
            response = client.chat.completions.create(
                model=deployment_name,
                messages=messages,
                temperature=0.7,
                stream=True
            )
            
            # Stream the response
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})