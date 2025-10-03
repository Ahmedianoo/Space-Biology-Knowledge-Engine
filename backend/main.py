from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import user 
from backend.routes import api

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow access from anywhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router, prefix="/user")
app.include_router(api.router, prefix="/api")

@app.get("/")
def hello_world():
    return {"message": "zuma and niazi are fucking the back"}
