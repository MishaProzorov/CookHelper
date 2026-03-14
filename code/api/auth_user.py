from fastapi import APIRouter, Depends
from services import user_service as service
from schemas import UserClass

router = APIRouter()

@router.post("/registration")
def creat_user(res = Depends(service.creat_user)):
    return res

@router.post("/login")
def login_user(res = Depends(service.login_user)):
    return res

@router.get("/registration/", response_model=list[UserClass])
def return_user(res = Depends(service.return_user)):
    return res

@router.get("/registration/{id}", response_model=UserClass)
def return_one_user(res = Depends(service.return_one_user)):
    return res

@router.delete("/registration/{id}")
def delete_user(res = Depends(service.delete_user)):
    return res

@router.put("/registration/{id}")
def change_user(res = Depends(service.change_user)):
    return res