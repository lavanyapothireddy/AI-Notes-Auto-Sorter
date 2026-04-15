from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.ai_sorter import sort_notes

app = FastAPI()

# ✅ Enable CORS
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

# ✅ Root (now shows message instead of index.html)
@app.get("/")
def home():
    return {"message": "🚀 AI Notes Auto-Sorter is running"}

# ✅ Health check
@app.get("/status")
def status():
    return {"message": "✅ Backend is live and working"}

# ✅ Main API
@app.post("/sort-notes")
def sort_user_notes(data: NotesInput):
    try:
        result = sort_notes(data.notes)
        return {"sorted_notes": result}
    except Exception as e:
        return {"sorted_notes": {}, "error": str(e)}
