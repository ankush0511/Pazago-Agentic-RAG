from agno.models.google import Gemini
# from agno.document.chunking.agentic import 
from agno.embedder.google import GeminiEmbedder
from agno.vectordb.chroma import ChromaDb
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader

import os
from dotenv import load_dotenv
load_dotenv()
from agno.agent import Agent

api_key=os.getenv("PINECONE_API_KEY")
index="berkshire-hathaway-rag"
vector_db=ChromaDb(
    collection='rag',
    path='tmp/chroma',
    persistent_client=True,
)

storage=SqliteStorage(table_name='agent_session',db_file="tmp/storage.db")
memory_db=SqliteMemoryDb(table_name='memory',db_file="tmp/memory.db")

memory=Memory(db=memory_db)


knowledge_base=PDFKnowledgeBase(
    name="Berkshire Hathaway Letters",
    path="2024.pdf",
    vector_db=vector_db,
    dimension=1536,
    reader=PDFReader(chunk=True)
)


knowledge_base.load(recreate=False)
from agno.models.openai import OpenAIChat
from agno.agent import Agent
import os
from dotenv import load_dotenv
load_dotenv()

user_id='ankush',
session_id='ank@gmail.com'

rag_agent=Agent(
    name="RAG Agent",
    model=OpenAIChat(
    api_key=os.getenv("OPENAI_API_KEY"),
    id="gpt-5"
),
    instructions= """You are a knowledgeable financial analyst specializing in Warren Buffett's investment philosophy and Berkshire Hathaway's business strategy. Your expertise comes from analyzing years of Berkshire Hathaway annual shareholder letters stored in a Pinecone vector database.

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
    knowledge=knowledge_base,
    enable_agentic_memory=True,
    user_id=user_id,
    show_tool_calls=True,
    memory=memory,
    exponential_backoff=True,
    retries=3
)

# Run with streaming enabled
response_stream = rag_agent.run("what happened in 2024 and give the some insights from it").content
print(response_stream)

