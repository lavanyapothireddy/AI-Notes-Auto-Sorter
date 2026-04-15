from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from backend.ai_sorter import sort_notes

app = FastAPI()

# ✅ Enable CORS (needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Input model
class NotesInput(BaseModel):
    notes: list[str]

# ✅ Health check (VERY IMPORTANT for Render)
@app.get("/status")
def status():
    return {"message": "🚀 AI Notes Auto-Sorter is running"}

# ✅ Main API
@app.post("/sort-notes")
def sort_user_notes(data: NotesInput):
    try:
        result = sort_notes(data.notes)
        return {"sorted_notes": result}
    except Exception as e:
        return {"sorted_notes": {}, "error": str(e)}

# ✅ Serve frontend (index.html)
@app.get("/")
def home():
    file_path = os.path.join(os.path.dirname(__file__), "..", "index.html")
    
    # fallback safety
    if not os.path.exists(file_path):
        return {"message": "Frontend not found, but API is running 🚀"}
    
    return FileResponse(file_path)
