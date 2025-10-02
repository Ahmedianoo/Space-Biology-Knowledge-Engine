import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_publication(url: str) -> dict:
    """Scrape publication page and return dict with metadata + structured sections."""

    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "lxml")

    # ---- Metadata ----
    journal, date, authors = None, None, []

    citation_block = soup.find("section", {"class": "pmc-layout__citation"})
    if citation_block:
        text = citation_block.get_text(" ", strip=True)
        parts = text.split(".")
        if parts:
            journal = parts[0].strip()
        if len(parts) > 1:
            for token in parts[1].split():
                if token.isdigit() and len(token) == 4:
                    date = parts[1].strip()
                    break

    for span in soup.select("span.name.western"):
        authors.append(span.get_text(strip=True))

    # ---- Sections ----
    sections = []

    article_body = soup.select_one("section.body.main-article-body")
    if article_body:
        for sec in article_body.find_all("section", recursive=False):
            sec_id = sec.get("id", "")
            title_tag = sec.find(["h2", "h3"])
            title = title_tag.get_text(strip=True) if title_tag else "Untitled"

            # collect paragraphs inside this section
            content_parts = [
                p.get_text(" ", strip=True) for p in sec.find_all("p", recursive=True)
            ]
            content = "\n".join(content_parts).strip()

            if content:
                sections.append({
                    "id": sec_id,
                    "title": title,
                    "content": content,
                })

    # fallback: if no structured sections found
    if not sections:
        sections.append({
            "id": "full_text",
            "title": "Full Text",
            "content": " ".join(p.get_text(" ", strip=True) for p in soup.find_all("p")),
        })

    return {
        "metadata": {
            "journal": journal,
            "date": date,
            "authors": authors,
        },
        "sections": sections
    }
