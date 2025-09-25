# Berkshire Hathaway RAG Chatbot

A production-ready RAG (Retrieval-Augmented Generation) chatbot that analyzes Warren Buffett's shareholder letters to provide investment insights and business strategy advice.

## Features

- **Interactive Streamlit UI**: Clean, user-friendly chat interface
- **RAG Implementation**: Uses ChromaDB for vector storage and OpenAI for generation
- **Memory Management**: Maintains conversation context across sessions
- **Production Structure**: Organized codebase with proper separation of concerns

## Project Structure

```
rag/
├── src/
│   ├── config/
│   │   └── settings.py          # Configuration settings
│   ├── models/
│   │   └── rag_agent.py         # RAG agent implementation
│   ├── services/
│   │   └── chat_service.py      # Chat service logic
│   └── ui/
│       └── streamlit_app.py     # Streamlit UI
├── data/                        # PDF documents
├── tmp/                         # Database files
├── app.py                       # Main entry point
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment variables**:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   ```

3. **Add PDF documents**:
   Place your Berkshire Hathaway shareholder letters in the `data/` folder.

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Features

- Ask questions about Warren Buffett's investment philosophy
- Get insights from Berkshire Hathaway's business strategies
- Contextual conversations with memory
- Source citations from shareholder letters

## Example Queries

- "What are Warren Buffett's key investment principles?"
- "How did Berkshire Hathaway perform in 2024?"
- "What does Buffett think about market volatility?"
- "Explain Berkshire's acquisition strategy"