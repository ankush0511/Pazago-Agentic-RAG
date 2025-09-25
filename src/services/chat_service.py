import streamlit as st
from ..models.rag_agent import RAGAgent

class ChatService:
    def __init__(self):
        self.rag_agent = None
        self.agent = None
    
    @st.cache_resource
    def initialize_rag_agent(_self):
        """Initialize RAG agent (cached for performance)"""
        _self.rag_agent = RAGAgent()
        _self.rag_agent.initialize_knowledge_base(recreate=False)
        return _self.rag_agent
    
    def get_agent(self, user_id, session_id):
        """Get or create agent for user session"""
        if not self.rag_agent:
            self.rag_agent = self.initialize_rag_agent()
        
        if not self.agent:
            self.agent = self.rag_agent.create_agent(user_id, session_id)
        
        return self.agent
    
    def get_response(self, query, user_id, session_id):
        """Get response from RAG agent with memory context"""
        try:
            agent = self.get_agent(user_id, session_id)
            response = agent.run(query)
            return response.content
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_memory(self, user_id, session_id):
        """Clear agent memory for fresh start"""
        try:
            if self.agent:
                self.agent.memory.clear()
            return True
        except Exception as e:
            return False
    
    def get_memory_summary(self, user_id, session_id):
        """Get summary of conversation memory"""
        try:
            if self.agent and hasattr(self.agent, 'memory'):
                return len(self.agent.memory.get_all())
            return 0
        except:
            return 0