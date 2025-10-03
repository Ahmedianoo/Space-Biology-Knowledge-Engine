from sentence_transformers import SentenceTransformer

# Load a lightweight embedding model
_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """Return a vector embedding for text."""
    return _model.encode(text).tolist()
