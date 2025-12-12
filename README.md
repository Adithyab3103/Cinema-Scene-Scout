# 🦇 Cinema Scene Scout: The Batman Edition

A Retrieval-Augmented Generation (RAG) application that allows you to find specific scenes in "The Batman (2022)" by describing them in natural language. The system searches through movie subtitles using semantic search powered by Google's Gemini models.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- **Natural Language Search**: Describe scenes in plain English (e.g., "the part where he says he is vengeance")
- **Semantic Search**: Uses Google's embedding models to find relevant scenes based on meaning, not just keywords
- **Dual Interface**: 
  - Web UI via Streamlit for easy interaction
  - REST API via FastAPI for programmatic access
- **Sliding Window Processing**: Groups subtitle chunks with overlapping windows for better context retention
- **Vector Database**: Uses ChromaDB for efficient similarity search

## 🏗️ Architecture

The application uses a RAG (Retrieval-Augmented Generation) pipeline:

1. **Ingestion**: Subtitle file → Sliding window chunks → Embeddings → ChromaDB vector store
2. **Query**: User query → Embedding → Similarity search → Context retrieval → LLM generation → Answer

**Tech Stack:**
- **LLM**: Google Gemini 2.0 Flash
- **Embeddings**: Google Generative AI Embeddings (models/embedding-001)
- **Vector Store**: ChromaDB
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Framework**: LangChain

## 📁 Project Structure

```
directTest/
├── api.py                 # FastAPI backend server
├── app.py                 # Streamlit web interface
├── ingest.py              # Data ingestion script (run first)
├── rag_backend.py         # RAG chain implementation
├── requirements.txt       # Python dependencies
├── TheBatman2022.srt      # Subtitle file
├── .env                   # Environment variables (create this)
└── db/                    # ChromaDB database (created after ingestion)
```

## 🔧 Prerequisites

- Python 3.8 or higher
- Conda (recommended) or virtual environment
- Google API Key (get one from [Google AI Studio](https://makersuite.google.com/app/apikey))

## 📦 Installation

### Step 1: Set Up Environment

**Using Conda (Recommended):**
```bash
conda create -n scene-scout python=3.10
conda activate scene-scout
```

**Or using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Google API key to the `.env` file:

```
GOOGLE_API_KEY=your-google-api-key-here
```

> **Note**: The `.env` file is automatically ignored by git. Never commit your API key!

## 🚀 Usage

### Step 1: Ingest Subtitle Data

First, process the subtitle file to create the vector database:

```bash
python ingest.py
```

This will:
- Load the `TheBatman2022.srt` file
- Apply sliding window processing (window size: 3)
- Generate embeddings using Google's model
- Store everything in the `db/` directory

> **Note**: You only need to run this once. If you update the subtitle file, delete the `db/` folder and run `ingest.py` again.

### Step 2: Start the Backend API

In one terminal, start the FastAPI server:

```bash
uvicorn api:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Step 3: Launch the Web Interface

In another terminal, start the Streamlit app:

```bash
streamlit run app.py
```

The web interface will automatically open in your browser at `http://localhost:8501`

### Step 4: Search for Scenes

Type natural language queries like:
- "the part where he says he is vengeance"
- "scene with the car chase"
- "when batman first appears"

## 📡 API Documentation

### Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "message": "Cinema Scene Scout API is running."
}
```

#### `POST /search`
Search for scenes based on a natural language query.

**Request Body:**
```json
{
  "query": "the part where he says he is vengeance"
}
```

**Response:**
```json
{
  "answer": "The scene occurs at timestamp [00:15:32]..."
}
```

**Example using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "the part where he says he is vengeance"}'
```

**Example using Python:**
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/search",
    json={"query": "the part where he says he is vengeance"}
)
print(response.json()["answer"])
```

### Interactive API Docs

Once the FastAPI server is running, visit:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🔍 How It Works

1. **Ingestion Process** (`ingest.py`):
   - Loads the `.srt` subtitle file using LangChain's SRTLoader
   - Applies a sliding window of size 3 to create overlapping chunks (for better context)
   - Generates embeddings for each chunk using Google's embedding model
   - Stores embeddings and metadata in ChromaDB

2. **Query Process** (`rag_backend.py`):
   - User submits a natural language query
   - Query is embedded using the same embedding model
   - Performs similarity search in ChromaDB (retrieves top 20 matches)
   - Retrieved context is passed to Gemini 2.0 Flash LLM
   - LLM generates a natural language answer with timestamps

3. **Sliding Window**:
   - Groups consecutive subtitle chunks (default: 3 chunks)
   - Creates overlapping windows to preserve context across boundaries
   - Example: Chunks [1,2,3], [2,3,4], [3,4,5]...

## 🐛 Troubleshooting

### "Database folder 'db' not found"
- Run `python ingest.py` first to create the database

### "Google API key not found"
- Make sure you created a `.env` file with `GOOGLE_API_KEY=your-key`
- Check that the `.env` file is in the project root directory

### "Cannot connect to API" (Streamlit error)
- Make sure `uvicorn api:app --reload` is running in another terminal
- Check that the API is accessible at `http://127.0.0.1:8000`

### "Error loading SRT file"
- Verify that `TheBatman2022.srt` exists in the project root
- Check that the file is a valid SRT format

### API Rate Limits
- Google API has rate limits. If you hit limits, wait a few minutes and try again
- Consider using a different Google API key if needed

## 📝 Configuration Options

You can modify these settings in the code:

**In `ingest.py`:**
- `WINDOW_SIZE`: Number of subtitle chunks per window (default: 3)
- `PERSIST_DIRECTORY`: Database storage location (default: "db")

**In `rag_backend.py`:**
- `k`: Number of retrieved documents (default: 20)
- `model`: LLM model name (default: "gemini-2.0-flash")
- `temperature`: LLM temperature (default: 0)

## 🔐 Security Notes

- Never commit your `.env` file or API keys to version control
- The `.env` file should already be in `.gitignore`
- Keep your Google API key secure and rotate it if exposed

## 📄 License

This project is for educational purposes. The subtitle file (`TheBatman2022.srt`) is used for demonstration only.

## 🤝 Contributing

Feel free to fork this project and adapt it for other movies or use cases!

---

**Made with 🦇 for Batman fans**
