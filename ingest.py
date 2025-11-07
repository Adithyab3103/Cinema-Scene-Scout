import os
from langchain_community.document_loaders import SRTLoader
# --- CHANGED HERE ---
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import google.generativeai as genai

# --- Configuration ---
load_dotenv()

# --- CHANGED HERE: Check for Google API Key ---
if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("Google API key not found. Please set it in your .env file.")

# --- CHANGED HERE: Configure the API key for the library ---
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Script Parameters ---
SOURCE_FILE = "TheBatman2022.srt"
PERSIST_DIRECTORY = "db"

def ingest_data():
    """
    Reads the specified SRT file, generates embeddings using Google's model,
    and saves everything into a local vector database.
    """
    if not os.path.exists(SOURCE_FILE):
        print(f"--- 🚨 ERROR ---")
        print(f"Subtitle file not found at '{SOURCE_FILE}'")
        return

    print(f"Loading subtitle data from {SOURCE_FILE}...")
    loader = SRTLoader(SOURCE_FILE)
    documents = loader.load()
    print(f"✅ Successfully loaded {len(documents)} dialogue chunks.")

    print("\nCreating text embeddings with Google's model...")
    print("This might take a moment...")

    # --- CHANGED HERE: Use Google's embedding model ---
    # "models/embedding-001" is a powerful and free model for this task.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    print("Building the vector database...")
    db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )

    print("\n--------------------------------------------------")
    print("✅ Ingestion Complete!")
    print(f"The vector database has been created in the '{PERSIST_DIRECTORY}' directory.")
    print("You can now launch the web application by running:")
    print("streamlit run app.py")
    print("--------------------------------------------------")

if __name__ == "__main__":
    ingest_data()