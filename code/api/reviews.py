from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from database import get_db
from services import review_service as service

router = APIRouter()

@router.get("/api/reviews")
def get_reviews(db: Session = Depends(get_db)):
    return service.get_all_reviews(db)

@router.post("/api/reviews")
async def create_review(request: Request, text: str = Form(...), rating: int = Form(...), db: Session = Depends(get_db)):
    return await service.create_review(request, db, text, rating)

@router.delete("/api/reviews/{id}")
async def delete_review(id: int, request: Request, db: Session = Depends(get_db)):
    return await service.delete_review(id, request, db)
