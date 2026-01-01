# Nebulogy – Space Biology Knowledge Engine

## Overview
Nebulogy is an AI-powered web application that transforms NASA bioscience publications into actionable insights. It allows researchers, managers, and mission architects to efficiently explore role-specific summaries, knowledge graphs, and interactive dashboards.  

Developed during **NASA Space Apps Cairo Hackathon 2025** at Zewail City of Science and Technology.  

---

## Features
- **Semantic Search:** Search topics or publications; filter using tags (e.g., Mars, Moon, water, geology).  
- **Role-based Flashcards:**  
  - **Scientist:** methods, results, hypotheses  
  - **Manager:** broader impacts, investment potential  
  - **Mission Architect:** risks, requirements, insights  
  - Each flashcard links to the original NASA publication.  
- **Interactive Dashboards:** Knowledge graphs and analytical charts displaying connections and key metrics.  
- **Audio Guidance:** Explains charts and graphs for better UX.  
- **Chatbot:** Provides role-adapted answers to user queries, delivering explanations and insights tailored to whether you’re a scientist, manager, or mission architect.  
- **External Resources Access:** Explore NASA OSDR, NSLSL, and NASA Task Book.  

---

## Screenshots

![Dashboard](screenshots/dashboard.png)  
![Flashcard](screenshots/flashcard.png)  
![Search](screenshots/search.png)  
![Tag Filter](screenshots/tag_filter.png)  
![Knowledge Graph](screenshots/knowledge_graph.png)  
![Analytics Chart](screenshots/analytics_chart.png)  
![Audio Guidance](screenshots/audio_guidance.png)  
![Resources](screenshots/resources.png)  
![Chatbot](screenshots/chatbot.png)  


---

## Architecture
- **Frontend:** React.js  
- **Backend:** FastAPI  
- **Web Scraping:** Beautiful Soup  
- **Embeddings & Semantic Search:** Sentence Transformers + Milvus  
- **Summarization:** LangGraph  
- **LLM Calls:** Groq API  


---

## Installation

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install   # first time only
npm run dev
```

---

## Tech Stack
| Component      | Technology |
|----------------|------------|
| Frontend       | React.js   |
| Backend        | FastAPI    |
| Scraping       | Beautiful Soup |
| Embeddings & Search | Sentence Transformers + Milvus |
| Summarization  | LangGraph  |
| LLM Calls      | Groq API   |
