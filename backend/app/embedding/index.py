from app.db import SessionLocal
from app.models import Publication, PublicationSection
from app.embedding.chunker import chunk_text
from app.embedding.embed import get_embedding
from app.embedding.vector_store import create_collection_if_not_exists, insert_chunks


def index_publications():
    session = SessionLocal()
    create_collection_if_not_exists()

    pubs = session.query(Publication).all()
    for pub in pubs:
        for sec in pub.sections:
            chunks = chunk_text(sec.section_text, sec.section_name)
            embeddings = [get_embedding(ch) for ch in chunks]
            insert_chunks(pub.id, sec.section_name, chunks, embeddings)

        print(f"✅ Indexed publication: {pub.title}")

    session.close()


if __name__ == "__main__":
    print("🚀 Starting indexing of all publications...")
    index_publications()
    print("✅ Indexing completed.")
