from fastapi import APIRouter, Body

router = APIRouter(prefix="/user") 




@router.get("/")
def hello_world():
    return {"message": "welcome from user"}

