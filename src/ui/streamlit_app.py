import streamlit as st
import uuid
from ..services.chat_service import ChatService

class RAGChatbotApp:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "user_id" not in st.session_state:
            st.session_state.user_id = str(uuid.uuid4())
        if "session_id" not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if "chat_service" not in st.session_state:
            st.session_state.chat_service = ChatService()
    
    def run(self):
        """Run the Streamlit application"""
        st.title("💰 Berkshire Hathaway Investment Advisor")
        st.markdown("Ask questions about Warren Buffett's investment philosophy and Berkshire Hathaway's strategies based on shareholder letters.")
        st.caption("🧠 **Memory Enabled**: This chatbot remembers our conversation and provides contextual responses.")
        
        # Sidebar
        with st.sidebar:
            st.header("About")
            st.markdown("""
            This chatbot analyzes Warren Buffett's shareholder letters to provide insights on:
            - Investment philosophy
            - Business strategies
            - Market analysis
            - Company performance
            """)
            
            st.header("Memory & Context")
            st.info("🧠 This chatbot remembers your conversation history and maintains context across sessions.")
            
            # Memory controls
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Clear Chat"):
                    st.session_state.messages = []
                    st.rerun()
            
            with col2:
                if st.button("Reset Memory"):
                    if hasattr(st.session_state, 'chat_service') and st.session_state.chat_service.agent:
                        st.session_state.chat_service.agent.memory.clear()
                    st.session_state.messages = []
                    st.success("Memory cleared!")
                    st.rerun()
            
            # Show conversation count
            if st.session_state.messages:
                st.metric("Messages in Session", len(st.session_state.messages))
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Memory context indicator
        if st.session_state.messages:
            st.info(f"🧠 Conversation context: {len(st.session_state.messages)} messages | Memory active for personalized responses")
        
        # Chat input
        if prompt := st.chat_input("Ask about Warren Buffett's investment insights..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing shareholder letters with context..."):
                    response = st.session_state.chat_service.get_response(
                        prompt, 
                        st.session_state.user_id, 
                        st.session_state.session_id
                    )
                st.markdown(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})