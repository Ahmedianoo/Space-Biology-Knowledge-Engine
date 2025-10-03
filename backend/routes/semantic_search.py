from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import Publication, Summary
from app.embedding.vector_store import semantic_search

router = APIRouter(prefix="/search", tags=["Semantic Search"])

# Request schema
class SearchRequest(BaseModel):
    query: str
    tags: Optional[List[str]] = []

# Response schema
class SummaryResponse(BaseModel):
    publication_id: str
    title: str
    url: str
    num_authors: int
    summaries: dict  # {"scientist": {...}, "manager": {...}, "mission_architect": {...}}

@router.post("/", response_model=dict)
def get_top_summaries(request: SearchRequest, db: Session = Depends(get_db)):
    # 1️⃣ Build context-aware query for semantic search
    if request.tags:
        context_string = "The user is interested in publications related to: " + ", ".join(request.tags)
        combined_query = f"{request.query}. Context: {context_string}"
    else:
        combined_query = request.query

    # 2️⃣ Semantic search on Milvus
    top_chunks = semantic_search(combined_query, top_k=3)

    if not top_chunks:
        raise HTTPException(status_code=404, detail="No results found")

    # 3️⃣ Collect publication IDs
    pub_ids = list(set([c["publication_id"] for c in top_chunks]))

    # 4️⃣ Fetch publications & summaries from DB
    pubs = db.query(Publication).filter(Publication.id.in_(pub_ids)).all()

    response = []

    for pub in pubs:
        # Each author is stored 3x, divide to get unique count
        num_authors = len(pub.authors) // 3 if pub.authors else 0

        # Find corresponding summary
        summary_obj = db.query(Summary).filter(Summary.publication_id == pub.id).first()

        summaries = {}
        if summary_obj:
            summaries = {
                "scientist": summary_obj.scientist_summary or {},
                "manager": summary_obj.manager_summary or {},
                "mission_architect": summary_obj.mission_architect_summary or {}
            }

        response.append({
            "publication_id": str(pub.id),
            "title": pub.title,
            "url": pub.url,
            "num_authors": num_authors,
            "summaries": summaries
        })

    return {"results": response}
