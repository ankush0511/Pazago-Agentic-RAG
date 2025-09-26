import sys
import os
import streamlit as st

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.streamlit_app import RAGChatbotApp

# Configuration constants
PAGE_TITLE = "Berkshire Hathaway RAG Chatbot"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        layout=PAGE_LAYOUT,
        initial_sidebar_state=SIDEBAR_STATE,
        page_icon="💰"
    )
    
    # Initialize and run the application
    app = RAGChatbotApp()
    app.run()

if __name__ == "__main__":
    main()