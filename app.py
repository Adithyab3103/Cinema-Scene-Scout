import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import google.generativeai as genai

# --- Application Configuration ---
load_dotenv()
PERSIST_DIRECTORY = "db"

# --- Pre-launch Checks ---
# Check for the GOOGLE_API_KEY
if not os.getenv("GOOGLE_API_KEY"):
    st.error("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

# Configure the genai library with the API key
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    st.error(f"Error configuring Google API: {e}")
    st.stop()

# Check if the database directory exists
if not os.path.exists(PERSIST_DIRECTORY):
    st.error("Database not found. Please run 'python ingest.py' first to create the local database.")
    st.stop()

# --- Core RAG Logic ---
@st.cache_resource
def load_rag_chain():
    """
    Loads all the necessary components for the RAG chain using Google's models.[[']]
    """
    # 1. Load the Vector Database using Google's embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 5})

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

    # 3. Initialize the Language Model using Google's Gemini Pro
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

    # 4. Build the RAG Chain
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# --- Main Streamlit User Interface ---
st.set_page_config(page_title="Cinema Scene Scout", page_icon="🦇")
st.title("🦇 Cinema Scene Scout")
st.markdown("---")
st.subheader("Search for scenes in *The Batman (2022)*")
st.write("Describe a scene, and the AI will find the dialogue and timestamp for you.")
st.write("Example: _'the part where he says he is vengeance'_")

try:
    rag_chain = load_rag_chain()
except Exception as e:
    st.error(f"Failed to load the application components: {e}")
    st.stop()

user_query = st.text_input("Describe the scene you're looking for:", key="search_box")

# Replace the old 'if user_query:' block with this new one

if user_query:
    with st.spinner("Searching the shadows for your scene..."):
        try:
            # Use st.write_stream to display the output as it's generated
            st.write_stream(rag_chain.stream(user_query))
        except Exception as e:
            if "prompt was blocked" in str(e):
                 st.error("The response was blocked by Google's safety filters. Please try a different query.")
            else:
                 st.error(f"An error occurred while searching: {e}")