from pymilvus import connections, utility
import os
from dotenv import load_dotenv

load_dotenv()

connections.connect(
    "default",
    uri=os.getenv("ZILLIZ_CLOUD_URI"),
    token=os.getenv("ZILLIZ_API_KEY")
)

COLLECTION_NAME = "publication_chunks"  # change if your old one was named differently

if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)
    print(f"🗑️ Dropped collection: {COLLECTION_NAME}")
else:
    print(f"⚠️ Collection {COLLECTION_NAME} does not exist")
