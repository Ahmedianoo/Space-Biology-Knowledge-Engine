import json
from collections import Counter
from dateutil import parser
from app.db import SessionLocal
from app.models import Publication

# --- 1. Define broader categories with keywords ---
CATEGORY_KEYWORDS = {
    "Human Research": ["human", "muscle", "heart", "astronaut", "cardiac", "bone", "behavior", "cognitive"],
    "Plant Biology": ["plant", "seed", "growth", "flora", "photosynthesis", "crop"],
    "Microgravity Effects": ["microgravity", "weightless", "zero-g", "gravitational"],
    "Radiation Effects": ["radiation", "ionizing", "cosmic ray", "dna damage", "x-ray"],
    "Cellular & Molecular Biology": ["cell", "protein", "dna", "gene", "molecular", "enzyme"],
    "Animal Research": ["mouse", "rat", "zebrafish", "worm", "invertebrate", "model organism"],
    "Biochemistry & Metabolism": ["metabolism", "lipid", "enzyme", "hormone"],
    "Other": []
}

def categorize_title(title: str) -> str:
    title_lower = title.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in title_lower for keyword in keywords) and category != "Other":
            return category
    return "Other"

# --- 2. Connect to DB and read publications ---
session = SessionLocal()
publications = session.query(Publication).all()
session.close()

# --- 3. Categories ---
titles_categories = {pub.title: categorize_title(pub.title) for pub in publications}
category_counts = Counter(titles_categories.values())
category_chart_data = [{"category": cat, "count": count} for cat, count in category_counts.items()]

# --- 4. Timeline / Year counts ---
years = []
for pub in publications:
    if pub.date:
        try:
            year = parser.parse(pub.date, fuzzy=True).year
            years.append(year)
        except Exception:
            continue  # skip if date can't be parsed

year_counts = Counter(years)
timeline_chart_data = [{"year": y, "count": year_counts[y]} for y in sorted(year_counts)]

# --- 5. Journals ---
journals = [pub.journal for pub in publications if pub.journal]
journal_counts = Counter(journals)
journal_chart_data = [{"journal": j, "count": c} for j, c in journal_counts.items()]
distinct_journals_count = len(journal_counts)

# --- 6. Output JSON for frontend ---
output = {
    "category_chart": category_chart_data,
    "timeline_chart": timeline_chart_data,
    "journal_chart": journal_chart_data,
    "distinct_journals_count": distinct_journals_count
}

print(json.dumps(output, indent=2))
