from sqlalchemy.orm import Session
from backend.app.db import engine
from backend.app.models import PublicationSection, Research, Summary
from backend.Summaries.summarization_pipeline import app
import asyncio
import uuid

ROLE_PROMPTS = {
    "scientist": "Summarize the research focusing on technical details, methods, and scientific rigor.",
    "manager": "Summarize the research focusing on project outcomes, resources, and high-level implications.",
    "mission_planner": "Summarize the research focusing on logistics, feasibility, scheduling, and operational planning."
}

def get_research_sections(session):
    """Group section summaries by research_id"""
    sections = session.query(PublicationSection).all()
    research_map = {}
    for s in sections:
        if not s.section_summary:
            continue
        research_map.setdefault(s.research_id, []).append(s.section_summary)
    return research_map

async def generate_role_summary(research_id, combined, role):
    """LLM call for a role-specific summary"""
    prompt = f"{ROLE_PROMPTS[role]}\n\nResearch content:\n{combined}"
    result = await app.ainvoke({"contents": [prompt]})
    return result.get("final_summary", "").strip()

async def process_research():
    session = Session(bind=engine)

    research_map = get_research_sections(session)
    print(f"Found {len(research_map)} researches to summarize")

    for research_id, summaries in research_map.items():
        combined = " ".join(summaries)

        for role in ROLE_PROMPTS:
            try:
                summary_text = await generate_role_summary(research_id, combined, role)
                summary = Summary(
                    id=str(uuid.uuid4()),
                    research_id=research_id,
                    role=role,
                    summary=summary_text
                )
                session.add(summary)
                print(f"✅ {role} summary created for research {research_id}")
            except Exception as e:
                print(f"❌ Failed for {role}, research {research_id}: {e}")
                session.rollback()

    session.commit()
    session.close()

if __name__ == "__main__":
    asyncio.run(process_research())
