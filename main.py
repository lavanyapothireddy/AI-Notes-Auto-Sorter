from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from ai_sorter import sort_notes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotesInput(BaseModel):
    notes: list[str]

@app.post("/sort-notes")
def sort_user_notes(data: NotesInput):
    try:
        result = sort_notes(data.notes)
        return {"sorted_notes": result}
    except Exception as e:
        return {"sorted_notes": {}, "error": str(e)}

@app.get("/")
def home():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))