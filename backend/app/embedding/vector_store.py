from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

connections.connect(
    "default",
    uri=os.getenv("ZILLIZ_CLOUD_URI"),
    token=os.getenv("ZILLIZ_API_KEY")
)

COLLECTION_NAME = "publication_chunks"
EMBEDDING_DIM = 384  # MiniLM output size

def create_collection_if_not_exists():
    if utility.has_collection(COLLECTION_NAME):
        # ✅ check schema to avoid dim mismatch
        col = Collection(COLLECTION_NAME)
        for f in col.schema.fields:
            if f.name == "embedding" and f.params.get("dim") != EMBEDDING_DIM:
                print(f"⚠️ Collection exists with dim={f.params.get('dim')} instead of {EMBEDDING_DIM}. Dropping...")
                utility.drop_collection(COLLECTION_NAME)
                break
        else:
            # correct schema, nothing to do
            return

    fields = [
        FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=36, is_primary=True),
        FieldSchema(name="publication_id", dtype=DataType.VARCHAR, max_length=36),
        FieldSchema(name="section_name", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
    ]

    schema = CollectionSchema(fields, description="Publication chunks with embeddings")
    col = Collection(name=COLLECTION_NAME, schema=schema)

    index_params = {
        "metric_type": "COSINE",
        "index_type": "HNSW",
        "params": {"M": 8, "efConstruction": 64}
    }
    col.create_index(field_name="embedding", index_params=index_params)
    print(f"✅ Created collection `{COLLECTION_NAME}` with dim={EMBEDDING_DIM}")


def insert_chunks(pub_id: str, section_name: str, chunks: list, embeddings: list):
    col = Collection(COLLECTION_NAME)
    data = [
        [str(uuid.uuid4()) for _ in chunks],   # ids
        [str(pub_id) for _ in chunks],
        [section_name for _ in chunks],
        chunks,
        embeddings
    ]
    col.insert(data)
    col.flush()
