import os
import shutil
from langchain_community.document_loaders import SRTLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv
import google.generativeai as genai

# --- Configuration ---
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Script Parameters ---
SOURCE_FILE = "TheBatman2022.srt"
PERSIST_DIRECTORY = "db"
WINDOW_SIZE = 3

def ingest_data():
    """
    Reads the SRT file, applies sliding window grouping, generates embeddings, and saves to ChromaDB.
    """
    if not os.path.exists(SOURCE_FILE):
        print(f"🚨 ERROR: Subtitle file not found at '{SOURCE_FILE}'")
        return

    # Clear existing DB
    if os.path.exists(PERSIST_DIRECTORY):
        print(f"Removing old database at {PERSIST_DIRECTORY}...")
        shutil.rmtree(PERSIST_DIRECTORY)

    print(f"Loading subtitle data from {SOURCE_FILE}...")
    try:
        loader = SRTLoader(SOURCE_FILE)
        raw_documents = loader.load()
    except Exception as e:
        print(f"❌ Error loading SRT file: {e}")
        return

    print(f"✅ Loaded {len(raw_documents)} raw chunks.")

    if not raw_documents:
        print("❌ Error: No subtitle data found (empty file?).")
        return

    # --- SLIDING WINDOW LOGIC START ---
    print(f"Applying Sliding Window (Size={WINDOW_SIZE})...")
    windowed_documents = []

    # Handle cases where the file is shorter than the window (e.g., test files or 1-line files)
    if len(raw_documents) < WINDOW_SIZE:
        print(f"⚠️ Warning: Not enough chunks ({len(raw_documents)}) for window size ({WINDOW_SIZE}). Merging all into one.")
        combined_content = " ".join([doc.page_content for doc in raw_documents])
        combined_metadata = raw_documents[0].metadata.copy()
        windowed_documents.append(Document(page_content=combined_content, metadata=combined_metadata))
    
    else:
        # Standard sliding window for normal files
        for i in range(len(raw_documents) - WINDOW_SIZE + 1):
            window = raw_documents[i : i + WINDOW_SIZE]
            
            combined_content = " ".join([doc.page_content for doc in window])
            combined_metadata = window[0].metadata.copy()
            
            new_doc = Document(page_content=combined_content, metadata=combined_metadata)
            windowed_documents.append(new_doc)

    print(f"✅ Created {len(windowed_documents)} windowed chunks.")
    # --- SLIDING WINDOW LOGIC END ---

    print("Creating embeddings with Google's model...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    print("Building vector database...")
    db = Chroma.from_documents(
        documents=windowed_documents,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY
    )
    
    print("\n--------------------------------------------------")
    print("✅ Ingestion Complete!")
    print(f"Database created in '{PERSIST_DIRECTORY}'.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    ingest_data()