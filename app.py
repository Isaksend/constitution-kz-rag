import streamlit as st
import os
from app.db.vector_store import initialize_vector_store, store_chat_history
from app.processor.document_loader import process_multiple_files, process_constitution
from app.models.llm import setup_qa_chain


def main():
    st.set_page_config(
        page_title="Kazakhstan Constitution AI Assistant",
        page_icon="📜",
        layout="wide"
    )

    st.title("Kazakhstan Constitution AI Assistant")
    st.markdown("Ask questions about the Constitution of the Republic of Kazakhstan")

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None

    if "qa_chain" not in st.session_state:
        st.session_state.qa_chain = None

    # Sidebar for document uploads
    with st.sidebar:
        st.header("Upload Documents")
        st.write("Upload Constitution or related documents")

        uploaded_files = st.file_uploader(
            "Upload Constitution or related documents",
            accept_multiple_files=True,
            type=["pdf", "txt"]
        )

        if uploaded_files and st.button("Process Documents"):
            with st.spinner("Processing documents..."):
                try:
                    # Process uploaded files
                    documents = process_multiple_files(uploaded_files)

                    if documents:
                        # Initialize vector store with documents
                        vector_store = initialize_vector_store(documents)

                        # Update session state
                        st.session_state.vector_store = vector_store
                        st.session_state.qa_chain = setup_qa_chain(vector_store)

                        st.success(f"Documents processed successfully! ({len(documents)} chunks)")
                    else:
                        st.error("No documents were successfully processed.")
                except Exception as e:
                    st.error(f"Error processing documents: {e}")

        # Add a button to fetch Constitution from website
        if st.button("Fetch Constitution from Website"):
            with st.spinner("Fetching Constitution..."):
                try:
                    # Process constitution
                    constitution_docs = process_constitution()

                    if constitution_docs:
                        # Initialize vector store with documents
                        vector_store = initialize_vector_store(constitution_docs)

                        # Update session state
                        st.session_state.vector_store = vector_store
                        st.session_state.qa_chain = setup_qa_chain(vector_store)

                        st.success(f"Constitution fetched successfully! ({len(constitution_docs)} articles)")
                    else:
                        st.error("Failed to fetch Constitution from website. Please upload manually.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    # In your app.py, add this section
    with st.sidebar.expander("View Chat History"):
        try:
            with open("chat_history.txt", "r", encoding="utf-8") as f:
                chat_history = f.read()
            st.text_area("Previous Conversations", chat_history, height=300)
        except FileNotFoundError:
            st.write("No chat history available yet.")


    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the Constitution"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response
        with st.chat_message("assistant"):
            if not st.session_state.vector_store or not st.session_state.qa_chain:
                response = "Please upload and process documents first, or fetch the Constitution from the website."
                st.write(response)
            else:
                with st.spinner("Researching the Constitution..."):
                    try:
                        # Get response from QA chain
                        result = st.session_state.qa_chain({"query": prompt})
                        response = result.get("result", "I couldn't find a relevant answer in the uploaded documents.")

                        # Display response
                        st.write(response)

                        # Store chat history
                        store_chat_history(prompt, response)
                    except Exception as e:
                        response = f"Error generating response: {e}"
                        st.error(response)

            # Add assistant message to session state
            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()