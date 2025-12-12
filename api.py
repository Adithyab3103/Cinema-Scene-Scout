from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_backend import get_rag_chain

# Initialize App
app = FastAPI(title="Cinema Scene Scout API")

# Load Chain on Startup
try:
    chain = get_rag_chain()
    print("✅ RAG Chain loaded successfully.")
except Exception as e:
    print(f"❌ Error loading RAG Chain: {e}")
    chain = None

# Input Data Model
class QueryRequest(BaseModel):
    query: str

@app.get("/")
def home():
    return {"status": "online", "message": "Cinema Scene Scout API is running."}

@app.post("/search")
def search_scene(request: QueryRequest):
    if not chain:
        raise HTTPException(status_code=500, detail="System not initialized (Database missing?)")
    
    try:
        # Run the logic
        response = chain.invoke(request.query)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))