from sqlalchemy.orm import Session
from backend.app.db import engine
from backend.app.models import PublicationSection, Summary
from backend.Summaries.summarization_pipeline import app
import asyncio
import uuid


ROLE_PROMPTS = {
    "scientist": (
        "Provide a concise yet detailed summary of the research. "
        "Focus on the scientific background, objectives, hypothesis, "
        "methodology, experimental design, data analysis, key findings, "
        "and limitations. Emphasize technical rigor and relevance to the "
        "field, avoiding managerial or logistical perspectives."
    ),
    "manager": (
        "Summarize the research in a way that highlights strategic value. "
        "Focus on project objectives, key outcomes, return on investment, "
        "resource requirements, potential partnerships, and broader "
        "organizational or industry impact. Avoid deep technical jargon; "
        "emphasize practical results, cost-effectiveness, and scalability."
    ),
    "mission_architect": (
        "Summarize the research with an emphasis on operational planning. "
        "Highlight feasibility, logistical considerations, scheduling, "
        "resource allocation, potential risks, safety concerns, and "
        "dependencies. Provide insights relevant to execution, timelines, "
        "and contingency planning rather than technical details or funding strategy."
    )
}


def get_research_sections(session):
    """Group section summaries by publication_id, only rows with summaries"""
    sections = (
        session.query(PublicationSection)
        .filter(PublicationSection.section_summary.isnot(None))
        .limit(200)
        .all()
    )

    research_map = {}
    for s in sections:
        research_map.setdefault(s.publication_id, []).append(s.section_summary)
    return research_map

async def generate_role_summary(combined, role_prompt):
    """LLM call for a role-specific structured summary (dict by section)."""
    prompt = f"""
    {role_prompt}

    Research content:
    {combined}

    Please return the summary as a JSON object where each key is a section title
    (e.g., "Background", "Methodology", "Findings", "Implications")
    and each value is a concise summary for that section.
    Each section must not exceed 5 sentences.
    """
    result = await app.ainvoke({"contents": [prompt]})

    # try parsing JSON; if not valid, fallback to plain string
    text = result.get("final_summary", "").strip()
    try:
        import json
        parsed = json.loads(text)
        return parsed
    except Exception:
        return {"Full Summary": text}

async def process_research():
    session = Session(bind=engine)

    research_map = get_research_sections(session)
    print(f"Found {len(research_map)} publications to summarize")

    for publication_id, summaries in research_map.items():
        combined = " ".join(summaries)

        try:
            scientist = await generate_role_summary(combined, ROLE_PROMPTS["scientist"])
            manager = await generate_role_summary(combined, ROLE_PROMPTS["manager"])
            mission_architect = await generate_role_summary(combined, ROLE_PROMPTS["mission_architect"])

            # create one row in summaries table
            summary = Summary(
                publication_id=uuid.UUID(str(publication_id)),
                scientist_summary=scientist,
                manager_summary=manager,
                mission_architect_summary=mission_architect
            )
            session.add(summary)
            session.commit()  # commit per row
            print(f"✅ Summaries committed for publication {publication_id}")

        except Exception as e:
            session.rollback()
            print(f"❌ Failed for publication {publication_id}: {e}")

    session.close()



if __name__ == "__main__":
    asyncio.run(process_research())
