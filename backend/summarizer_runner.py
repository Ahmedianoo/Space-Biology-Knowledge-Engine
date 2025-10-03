from app.embedding.summarizer import generate_and_save_summaries

if __name__ == "__main__":
    pub_id = "YOUR_PUBLICATION_ID"  # replace with actual publication id
    generate_and_save_summaries(pub_id)
