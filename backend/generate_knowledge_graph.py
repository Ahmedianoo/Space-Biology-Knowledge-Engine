import random
import json
from app.db import SessionLocal
from app.models import Publication
from app.embedding.vector_store import semantic_search

def generate_related_knowledge_graph(top_k=5):
    session = SessionLocal()
    pubs = session.query(Publication).all()

    if not pubs:
        session.close()
        return {"nodes": [], "edges": []}

    # Pick a random seed publication
    seed_pub = random.choice(pubs)

    # Try semantic search for related pubs
    related_pubs = semantic_search(seed_pub.title, top_k=top_k * 2)

    # Fallback: pick random publications if semantic search returns nothing
    if not related_pubs:
        related_pubs = [
            {"publication_id": str(pub.id), "title": pub.title, "score": 0.0}
            for pub in random.sample(pubs, min(top_k, len(pubs)))
            if pub.id != seed_pub.id
        ]

    nodes = [{"id": str(seed_pub.id), "title": seed_pub.title, "summary": "Summary not available"}]
    added_pub_ids = {str(seed_pub.id)}
    edges = []

    for r in related_pubs:
        pub_id = str(r["publication_id"])
        if pub_id in added_pub_ids:
            continue

        nodes.append({"id": pub_id, "title": r["title"], "summary": "Summary not available"})
        added_pub_ids.add(pub_id)

        edges.append({"source": str(seed_pub.id), "target": pub_id, "weight": r.get("score", 0.0)})

        if len(nodes) >= top_k + 1:
            break

    session.close()
    return {"nodes": nodes, "edges": edges}

if __name__ == "__main__":
    graph_data = generate_related_knowledge_graph(top_k=5)
    with open("knowledge_graph.json", "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    print("✅ Knowledge graph JSON saved to knowledge_graph.json")
