from fastapi import FastAPI
from routes.chatbot import chat_router

app = FastAPI()

app.include_router(chat_router)

@app.get('/')
def hello_world():
    return {"message": "hello world"}



