import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import google.generativeai as genai

# --- Configuration ---
load_dotenv()
PERSIST_DIRECTORY = "db"

# --- Setup Google API ---
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")

try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    raise ValueError(f"Error configuring Google API: {e}")

def format_docs(docs):
    """
    Helper to join retrieved documents into a single string.
    """
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    """
    Initializes and returns the RAG chain using Google's Gemini models.
    """
    # 1. Load the Vector Database
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    if not os.path.exists(PERSIST_DIRECTORY):
        raise FileNotFoundError(f"Database folder '{PERSIST_DIRECTORY}' not found. Please run ingest.py first.")

    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    
    # INCREASED k=20: Retrieves more lines to ensure we get the full conversation context
    retriever = db.as_retriever(search_kwargs={"k": 20})

    # 2. Create the Prompt Template
    template = """
    You are a helpful movie assistant. Your task is to find a specific scene based on the user's description.
    Use the following pieces of retrieved context, which contain dialogue and timestamps, to answer the user's question.
    
    If you don't find a relevant scene in the provided context, just say that you couldn't find a matching scene.
    Provide a clear, direct answer, quoting the dialogue and mentioning the exact start time.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 3. Initialize the Language Model
    # Switched to gemini-1.5-flash for stability. Change back to 2.0 only if you have specific access.
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

    # 4. Build the RAG Chain
    # Added 'format_docs' to clean up the retriever output before sending to LLM
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain