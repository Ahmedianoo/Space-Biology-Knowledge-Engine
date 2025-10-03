from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Client
from app.embedding.vector_store import semantic_search  # <- your search function

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found!")

chat_router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

client = Client(api_key=GROQ_API_KEY)

class QuestionRequest(BaseModel):
    question: str
    context: str = ""  # previous conversation / history


def prepare_context(query: str, top_k: int = 5) -> str:
    """
    Perform semantic search and return concatenated context text for the LLM.
    """
    chunks = semantic_search(query, top_k=top_k)
    context_texts = []
    for c in chunks:
        snippet = (
            f"Publication ID: {c['publication_id']}\n"
            f"Title: {c['title']}\n"
            f"Date: {c['date']}\n"
            f"Section: {c['section_name']}\n"
            f"Text: {c['text']}\n"
            "----"
        )
        context_texts.append(snippet)
    return "\n".join(context_texts)


def ask_groq_llm(system_prompt: str, user_question: str, semantic_context: str, history: str = ""):
    """
    Send question + semantic search context + history to the LLM.
    """
    # Add instructions to format output nicely
    system_message = {
        "role": "system",
        "content": (
            system_prompt +
            "If needed and according to the context and the question .Format your answer clearly with headings, subheadings, bullet points, numbered lists, "
            "and markdown where appropriate. Make it readable and structured, as if writing a report. "
            "Cite relevant publications by title from the context if possible."
        )
    }

    user_message = {
        "role": "user",
        "content": (
            f"Previous conversation:\n{history}\n\n"
            f"Relevant publications:\n{semantic_context}\n\n"
            f"User Question:\n{user_question}"
        )
    }

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[system_message, user_message],
        temperature=0.7
    )

    return completion.choices[0].message.content


@chat_router.post("/scientific")
def scientific_response(request: QuestionRequest):
    try:
        semantic_context = prepare_context(request.question, top_k=5)

        system_prompt = (
            "You are a highly knowledgeable AI assistant specialized in space science "
            "and space biology, referencing authoritative NASA publications. "
            "Provide scientific, detailed, analytical, and insightful answers."
        )

        answer = ask_groq_llm(system_prompt, request.question, semantic_context, request.context)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post("/investing")
def investing_response(request: QuestionRequest):
    try:
        semantic_context = prepare_context(request.question, top_k=5)

        system_prompt = (
            "You are a highly knowledgeable AI assistant specialized in finance and investment, "
            "with a focus on space technology, space biology, and aerospace sectors. "
            "Provide detailed, analytical, and insightful advice for investors, including "
            "risk assessment, market trends, and potential returns."
        )

        answer = ask_groq_llm(system_prompt, request.question, semantic_context, request.context)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post("/planner")
def planner_response(request: QuestionRequest):
    try:
        semantic_context = prepare_context(request.question, top_k=5)

        system_prompt = (
            "You are a highly knowledgeable AI assistant specialized in planning, project management, "
            "and strategic scheduling within space science and space biology projects. "
            "Provide detailed, structured, and practical guidance to help plan tasks, timelines, "
            "and resources efficiently."
        )

        answer = ask_groq_llm(system_prompt, request.question, semantic_context, request.context)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
