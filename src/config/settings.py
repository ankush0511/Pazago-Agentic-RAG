import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class Settings:
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

    # Database settings
    CHROMA_PATH = "tmp/chroma"
    STORAGE_DB = "tmp/storage.db"
    MEMORY_DB = "tmp/memory.db"
    
    # Vector DB settings
    COLLECTION_NAME = "rag"
    VECTOR_DIMENSION = 1536
    
    # Model settings
    MODEL_ID = "gpt-4"
    
    # Knowledge base settings
    PDF_PATH = "data"
    KNOWLEDGE_BASE_NAME = "Berkshire Hathaway Letters"

settings = Settings()