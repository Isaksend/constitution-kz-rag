from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Constitution-specific prompt template
CONSTITUTION_PROMPT = """
You are an AI assistant specializing in the Constitution of the Republic of Kazakhstan.
Answer the question based only on the context provided below.
Always cite specific articles in your response by referring to their article numbers.
If the information is not found in the provided context, state that you cannot find
relevant provisions in the Constitution.

Context:
{context}

Question: {question}

Answer:
"""


def get_ollama_llm(model_name="llama3"):
    """Get Ollama LLM instance"""
    return Ollama(model=model_name, base_url="http://localhost:11434")


def setup_qa_chain(vector_store):
    """Set up the QA chain with Ollama"""
    if not vector_store:
        return None

    # Initialize Ollama LLM
    llm = get_ollama_llm()

    # Create prompt template
    prompt = PromptTemplate(
        template=CONSTITUTION_PROMPT,
        input_variables=["context", "question"]
    )

    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain