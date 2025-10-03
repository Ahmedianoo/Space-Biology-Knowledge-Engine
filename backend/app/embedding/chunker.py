import re
from typing import List

def chunk_text(
    text: str, 
    title: str, 
    date: str, 
    section_name: str, 
    chunk_size: int = 750, 
    overlap: int = 50
) -> List[str]:
    """Split text into overlapping chunks and prepend metadata into each chunk."""
    text = re.sub(r"\s+", " ", text).strip()
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text = (
            f"[Title: {title}, Date: {date}, Section: {section_name}] "
            + " ".join(chunk_words)
        )
        chunks.append(chunk_text)
        start += chunk_size - overlap
    return chunks
