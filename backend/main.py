from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chatbot import chat_router
from routes import user 
from routes import api
from routes import semantic_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow access from anywhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

app.include_router(user.router)
app.include_router(api.router)
app.include_router(semantic_search.router)

@app.get('/')
def hello_world():
    return {"message": "hello world"}

