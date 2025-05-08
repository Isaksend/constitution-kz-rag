# Kazakhstan Constitution AI Assistant

An AI-powered assistant that can answer questions about the Constitution of the Republic of Kazakhstan using Retrieval-Augmented Generation (RAG) technology.

## Features

- Chat interface for asking questions about the Constitution of Kazakhstan
- Document upload functionality for the Constitution and related documents
- Vector-based search for accurate retrieval of constitutional information
- Chat history logging for reference and review
- Integration with local LLM (Ollama) for privacy and performance

## Screenshots

Constitution AI Assistant Interface ![image](https://github.com/user-attachments/assets/0f65fe09-5535-4c85-b284-fe2d5087e9a0)
Document Processing ![image](https://github.com/user-attachments/assets/a25566c5-4bf2-4baf-9644-c2d1d493f863)
Question Answering ![image](https://github.com/user-attachments/assets/87c769c8-ab7e-473a-ba9a-625dba7e84f9)
![image](https://github.com/user-attachments/assets/84707560-c7e0-4a10-8bf0-aab358d05ff7)


## Technologies Used

- **Streamlit**: For the web interface
- **LangChain**: For document processing and retrieval pipelines
- **Chroma**: For vector storage
- **Ollama**: For running the LLM locally
- **HuggingFace Embeddings**: For generating document embeddings

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/constitution-ai-assistant.git
   cd constitution-ai-assistant
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install Ollama from [https://ollama.ai/](https://ollama.ai/)

5. Pull the Llama model:
   ```
   ollama pull llama3
   ```

## Usage

1. Start the application:
   ```
   streamlit run app.py
   ```

2. Upload the Constitution document (PDF or TXT format) using the sidebar

3. Click "Process Documents" to analyze the Constitution

4. Ask questions about the Constitution in the chat interface

5. View chat history in the "chat_history.txt" file

## Example Questions

- "What are the official languages of Kazakhstan according to the Constitution?"
- "What rights and freedoms are guaranteed to citizens in the Constitution?"
- "How is the government structured according to the Constitution?"
- "What does the Constitution say about the judicial system and the role of judges?"
- "How can the Constitution be amended?"

## Project Structure

```
constitution-ai-assistant/
├── app.py                 # Main Streamlit application
├── app/
│   ├── __init__.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── vector_store.py # Vector storage implementation
│   ├── models/
│   │   ├── __init__.py
│   │   └── llm.py         # LLM integration
│   └── processor/
│       ├── __init__.py
│       └── document_loader.py # Document processing
├── chroma_db/             # Local vector store data
├── chat_history.txt       # Saved conversation history
└── requirements.txt       # Project dependencies
```

## Requirements

- Python 3.8+
- Ollama (with Llama3 model)
- 8GB+ RAM for embedding model

## License

MIT License

## Acknowledgements

- Built for the Blockchain Technologies 2 course
- Uses the official Constitution of the Republic of Kazakhstan
- Based on RAG (Retrieval Augmented Generation) architecture

## Future Improvements

- Add support for multiple languages
- Implement more advanced document preprocessing
- Add support for document comparison
- Improve citation of specific articles in responses
