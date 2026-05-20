from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from backend.graph.research_graph  import run_research
from backend.memory.memory_manager import get_all_sessions

router = APIRouter()

# Now accepts a LIST of questions instead of one
class ResearchRequest(BaseModel):
    questions: List[str]   # e.g. ["What is AI?", "What is blockchain?"]

@router.get("/")
def home():
    return {"message": "Research Assistant API is running!"}

@router.post("/research")
def research(request: ResearchRequest):

    results = []   # will hold all reports

    for question in request.questions:

        # Skip empty questions
        if not question.strip():
            continue

        print(f"\n📥 Researching: {question}")

        # Run the full pipeline for each question
        report = run_research(question)

        # Save each result
        results.append({
            "question": question,
            "report"  : report
        })

        print(f"✅ Done: {question}")

    return {
        "total"  : len(results),
        "results": results
    }

@router.get("/history")
def history():
    sessions = get_all_sessions()
    return {
        "total"   : len(sessions),
        "sessions": sessions
    }