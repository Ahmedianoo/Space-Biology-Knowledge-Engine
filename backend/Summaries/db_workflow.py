from sqlalchemy.orm import Session
from backend.app.db import engine
from backend.app.models import PublicationSection
from backend.Summaries.summarization_pipeline import app   # ✅ import the pipeline

import asyncio

session = Session(bind=engine)

#sections = session.query(PublicationSection).all()
def chunk_text(text, max_chars=3000):
    return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

async def summarize_long_text(text):
    chunks = chunk_text(text)
    partial_summaries = []

    for chunk in chunks:
        result = await app.ainvoke({"contents": [chunk]})
        partial_summaries.append(result.get("final_summary", "").strip())

    # Now summarize the summaries
    return " ".join(partial_summaries).strip()
    # final_result = await app.ainvoke({"contents": [combined]})
    # return final_result.get("final_summary", "").strip()

async def summarize_sections(batch_size=10):
    while True:
        sections = (
            session.query(PublicationSection)
            .filter(PublicationSection.section_summary == None)
            .limit(batch_size)
            .all()
        )

        if not sections:
            break

        for section in sections:
            try:
                summary = await summarize_long_text(section.section_text)
                section.section_summary = summary
                session.add(section)
                session.commit()
                print(f"✅ Section {section.id} summarized")
            except Exception as e:
                print(f"❌ Error with section {section.id}: {e}")
                session.rollback()

# async def summarize_sections(batch_size=10):
#     offset = 10
#     while True:
#         sections = (
#             session.query(PublicationSection)
#             .filter(PublicationSection.section_summary == None)  # ✅ only unsummarized
#             .offset(offset)
#             .limit(batch_size)
#             .all()
#         )

#         if not sections:
#             break  # no more rows

#         for section in sections:
#             try:
#                 summary = await summarize_long_text(section.section_text)
#                 section.section_summary = summary
#                 session.add(section)
#                 session.commit()
#                 print(f"✅ Section {section.id} summarized")
#             except Exception as e:
#                 print(f"❌ Error with section {section.id}: {e}")
#                 session.rollback()

#         offset += batch_size  # move to next batch

asyncio.run(summarize_sections())
