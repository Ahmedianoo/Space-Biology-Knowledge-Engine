import uuid
from app.models import Publication, PublicationSection

def save_publication(session, title, url, result: dict):
    metadata = result.get("metadata", {})
    sections = result.get("sections", [])

    pub = Publication(
        id=uuid.uuid4(),
        title=title,
        url=url,
        journal=metadata.get("journal"),
        date=metadata.get("date"),
        authors=metadata.get("authors"),  # JSON or Text field
    )
    session.add(pub)
    session.flush()  # ensures pub.id is available

    for section in sections:
        section_title = section.get("title") or "Untitled"
        section_text = section.get("content", "").strip()
        if not section_text:
            continue

        sec = PublicationSection(
            id=uuid.uuid4(),
            publication_id=pub.id,
            section_name=section_title,
            section_text=section_text
        )
        session.add(sec)

    session.commit()
    print(f"✅ Saved: {title}")
