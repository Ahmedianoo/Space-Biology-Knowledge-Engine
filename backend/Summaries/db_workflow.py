from sqlalchemy.orm import Session
from backend.app.db import engine
from backend.app.models import PublicationSection
from summarization_pipeline import app   # ✅ import the pipeline

import asyncio

session = Session(bind=engine)

sections = session.query(PublicationSection).all()

async def summarize_sections():
    for section in sections:
        result = await app.ainvoke({"contents": [section.section_text]})
        section.section_summary = result["final_summary"]
        session.add(section)
    session.commit()

asyncio.run(summarize_sections())
