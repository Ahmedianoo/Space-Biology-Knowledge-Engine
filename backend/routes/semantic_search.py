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
    summaries: List[dict]  # Each dict: {"scientist": {...}, "manager": {...}, "mission_architect": {...}}

@router.post("/", response_model=dict)
def get_top_summaries(request: SearchRequest, db: Session = Depends(get_db)):
    """
    Returns top 3 relevant publications for a given query and optional tags.
    Each publication includes up to 3 summaries, each with three role-based summaries.
    """
    # 1️⃣ Build context-aware query for semantic search
    combined_query = request.query
    if request.tags:
        context_string = "The user is interested in publications related to: " + ", ".join(request.tags)
        combined_query += f". Context: {context_string}"

    # 2️⃣ Semantic search on Milvus (get more chunks to cover multiple summaries)
    top_chunks = semantic_search(combined_query, top_k=20)
    if not top_chunks:
        raise HTTPException(status_code=404, detail="No results found")

    # 3️⃣ Collect unique publication IDs in order of relevance
    unique_pub_ids = []
    for chunk in top_chunks:
        if chunk["publication_id"] not in unique_pub_ids:
            unique_pub_ids.append(chunk["publication_id"])

    # Take top 3 publications
    top_pub_ids = unique_pub_ids[:3]

    # 4️⃣ Fetch publications from DB
    pubs = db.query(Publication).filter(Publication.id.in_(top_pub_ids)).all()
    pubs_map = {str(pub.id): pub for pub in pubs}

    response = []

    for pub_id in top_pub_ids:
        pub = pubs_map.get(pub_id)
        if not pub:
            continue

        num_authors = len(pub.authors) // 3 if pub.authors else 0

        # Fetch up to 3 summaries per publication
        summaries_objs = db.query(Summary).filter(Summary.publication_id == pub.id).limit(3).all()
        pub_summaries = []
        for summary_obj in summaries_objs:
            pub_summaries.append({
                "scientist": summary_obj.scientist_summary or {},
                "manager": summary_obj.manager_summary or {},
                "mission_architect": summary_obj.mission_architect_summary or {}
            })

        response.append({
            "publication_id": str(pub.id),
            "title": pub.title,
            "url": pub.url,
            "num_authors": num_authors,
            "summaries": pub_summaries
        })

    return {"results": response}
