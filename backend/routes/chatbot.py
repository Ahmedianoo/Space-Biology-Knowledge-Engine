from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Client

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found!")

chat_router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

client = Client(api_key=GROQ_API_KEY)  # initialize client

class QuestionRequest(BaseModel):
    question: str
    context: str = ""  # optional

@chat_router.post("/scientific")
def scientific_response(request: QuestionRequest):
    try:
        system_message = {
            "role": "system",
            "content": (
                "You are a highly knowledgeable AI assistant specialized in space science "
                "and space biology, referencing authoritative NASA publications. "
                "Provide scientific, detailed, analytical, and insightful answers. "
                "If information is missing in the context, indicate it clearly."
            )
        }

        user_message = {
            "role": "user",
            "content": (
                f"Context from NASA publications:\n{request.context}\n\n"
                f"Scientist's Question:\n{request.question}"
            )
        }

        # Call Groq chat API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[system_message, user_message],
            temperature=0.7
        )

        # Access content as an attribute, not as a dict
        answer = completion.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@chat_router.post("/investing")
def investing_response(request: QuestionRequest):
    try:
        system_message = {
            "role": "system",
            "content": (
                "You are a highly knowledgeable AI assistant specialized in finance and investment, "
                "with a focus on space technology, space biology, and aerospace sectors. "
                "Provide detailed, analytical, and insightful advice for investors, including "
                "risk assessment, market trends, and potential returns. "
                "Use research and data from authoritative NASA publications to support your insights. "
                "If information is missing in the context, indicate it clearly."
            )
        }

        user_message = {
            "role": "user",
            "content": (
                f"Context from NASA publications:\n{request.context}\n\n"
                f"Scientist's Question:\n{request.question}"
            )
        }

        # Call Groq chat API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[system_message, user_message],
            temperature=0.7
        )

        # Access content as an attribute, not as a dict
        answer = completion.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.post("/planner")
def planner_response(request: QuestionRequest):
    try:
        system_message = {
            "role": "system",
            "content": (
                    "You are a highly knowledgeable AI assistant specialized in planning, project management, "
                    "and strategic scheduling within space science and space biology projects. "
                    "Provide detailed, structured, and practical guidance to help plan tasks, timelines, "
                    "and resources efficiently. Use authoritative NASA research and publications to inform "
                    "your recommendations. If information is missing in the context, indicate it clearly."
            )
        }

        user_message = {
            "role": "user",
            "content": (
                f"Context from NASA publications:\n{request.context}\n\n"
                f"Scientist's Question:\n{request.question}"
            )
        }

        # Call Groq chat API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[system_message, user_message],
            temperature=0.7
        )

        # Access content as an attribute, not as a dict
        answer = completion.choices[0].message.content

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
