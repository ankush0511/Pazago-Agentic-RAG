from agno.models.openai import OpenAIChat
from agno.agent import Agent
from agno.document.chunking.agentic import AgenticChunking
from agno.vectordb.chroma import ChromaDb
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from ..config.settings import settings

class RAGAgent:
    def __init__(self):
        self.vector_db = ChromaDb(
            collection=settings.COLLECTION_NAME,
            path=settings.CHROMA_PATH,
            persistent_client=True,
        )
        
        self.storage = SqliteStorage(
            table_name='agent_session',
            db_file=settings.STORAGE_DB
        )
        
        self.memory_db = SqliteMemoryDb(
            table_name='memory',
            db_file=settings.MEMORY_DB
        )
        
        self.memory = Memory(db=self.memory_db)
        
        self.knowledge_base = PDFKnowledgeBase(
            name=settings.KNOWLEDGE_BASE_NAME,
            path="2022-merged.pdf",
            vector_db=self.vector_db,
            dimension=settings.VECTOR_DIMENSION,
            reader=PDFReader(chunk=True),
            chunking_strategy=AgenticChunking(),
        )
        
        self.agent = None
    
    def initialize_knowledge_base(self, recreate=False):
        """Initialize and load the knowledge base"""
        self.knowledge_base.load(recreate=recreate)
    
    def create_agent(self, user_id, session_id):
        """Create and return the RAG agent"""
        self.agent = Agent(
            name="RAG Agent",
            model=OpenAIChat(
                api_key=settings.OPENAI_API_KEY,
                id=settings.MODEL_ID
            ),
            instructions=self._get_instructions(),
            knowledge=self.knowledge_base,
            enable_agentic_memory=True,
            enable_user_memories=True,
            add_history_to_messages=True,
            session_id=session_id,
            user_id=user_id,
            show_tool_calls=True,
            memory=self.memory,
            exponential_backoff=True,
            retries=3,
            # debug=True            
        )
        return self.agent
    
    def _get_instructions(self):
        return """You are a knowledgeable financial analyst specializing in Warren Buffett's investment philosophy and Berkshire Hathaway's business strategy. Your expertise comes from analyzing years of Berkshire Hathaway annual shareholder letters stored in a Pinecone vector database.

    Core Responsibilities:
    • Answer questions about Warren Buffett's investment principles and philosophy
    • Provide insights into Berkshire Hathaway's business strategies and decisions
    • Reference specific examples from the shareholder letters when appropriate
    • Maintain context across conversations for follow-up questions
    • Analyze temporal trends and evolution of strategies across years

    Available Tools:
    1. vector_search: General semantic search across all letters
    2. temporal_analysis: Compare topics across multiple years
    3. year_search: Focus on specific year's letter

    Guidelines:
    • Always ground your responses in the provided shareholder letter content
    • Quote directly from the letters when relevant, with proper citations
    • If information isn't available in the documents, clearly state this limitation
    • Provide year-specific context when discussing how views or strategies evolved
    • For numerical data or specific acquisitions, cite the exact source letter and year
    • Use temporal analysis for questions about evolution or changes over time
    • Explain complex financial concepts in accessible terms while maintaining accuracy

    Response Format:
    • Provide comprehensive, well-structured answers
    • Include relevant quotes from the letters with year attribution
    • List source documents used for your response with relevance scores
    • For follow-up questions, reference previous conversation context appropriately
    • When analyzing trends, present information chronologically

    Search Strategy:
    • For general questions: Use vector_search with broad query
    • For evolution/trend questions: Use temporal_analysis with specific years
    • For year-specific questions: Use year_search for focused results
    • Combine multiple searches when needed for comprehensive analysis

    Remember: Your authority comes from the shareholder letters stored in Pinecone. Stay grounded in this source material and be transparent about the scope and limitations of your knowledge.""",
    