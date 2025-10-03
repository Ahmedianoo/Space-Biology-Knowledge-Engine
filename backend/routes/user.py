from fastapi import APIRouter, Body

router = APIRouter() 




@router.get("/")
def hello_world():
    return {"message": "welcome from user"}

