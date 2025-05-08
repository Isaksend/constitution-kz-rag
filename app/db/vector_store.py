from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from datetime import datetime
import os
import tempfile

# Directory to store Chroma database
CHROMA_PERSIST_DIRECTORY = "chroma_db"


def initialize_vector_store(documents=None):
    """Initialize a Chroma vector store with documents"""
    # Initialize embedding model
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Make sure the directory exists
    os.makedirs(CHROMA_PERSIST_DIRECTORY, exist_ok=True)

    # If documents are provided, create a vector store
    if documents:
        # Create vector store with documents
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=CHROMA_PERSIST_DIRECTORY
        )
        # Persist to disk
        vector_store.persist()
        return vector_store
    else:
        # Connect to existing vector store
        vector_store = Chroma(
            embedding_function=embedding_model,
            persist_directory=CHROMA_PERSIST_DIRECTORY
        )
        return vector_store


def search_documents(vector_store, query, k=3):
    """Search for relevant documents in vector store"""
    return vector_store.similarity_search(query, k=k)


def store_chat_history(question, answer):
    """Store chat history in a text file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # For logging purposes - store in a text file
    with open("chat_history.txt", "a", encoding="utf-8") as f:
        f.write(f"Time: {timestamp}\n")
        f.write(f"Question: {question}\n")
        f.write(f"Answer: {answer}\n")
        f.write("-" * 50 + "\n")

    print(f"Chat history stored: Q: {question}")