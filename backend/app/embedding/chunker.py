import re
from typing import List

def chunk_text(text: str, section_name: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = f"[Section: {section_name}] " + " ".join(chunk_words)
        chunks.append(chunk_text)
        start += chunk_size - overlap
    return chunks
