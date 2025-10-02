# app/scraper/run_scraper.py
import os
import pandas as pd
from app.scraper.fetcher import fetch_publication
from app.scraper.ingest import save_publication
from app.db import SessionLocal
from app.models import Publication

def main():
    # Resolve CSV path
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    CSV_PATH = os.path.join(BASE_DIR, "data", "SB_publication_PMC.csv")

    df = pd.read_csv(CSV_PATH)  # must have 'Title' and 'Link' columns

    session = SessionLocal()
    for _, row in df.iterrows():
        title, url = row["Title"], row["Link"]

        # Skip if already exists
        if session.query(Publication).filter_by(url=url).first():
            print(f"⏩ Skipping {title} (already in DB)")
            continue

        # Scrape
        result = fetch_publication(url)
        if not result or not result.get("sections"):
            print(f"❌ Failed to extract sections from {url}")
            continue


        # Save to DB
        save_publication(session, title, url, result)

    session.close()

if __name__ == "__main__":
    main()
