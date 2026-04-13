from fastapi import Request, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from models import Review, User
from database import get_db
from auth import security


async def get_current_user(request: Request, db: Session):
    """Получить текущего пользователя из токена в cookie."""
    token_data = await security.get_token_from_request(request, optional=True)
    if not token_data or not token_data.token:
        return None
    try:
        payload = security._decode_token(token_data.token)
        user_id = int(payload.sub)
        return db.query(User).filter(User.id == user_id).first()
    except Exception:
        return None


def get_all_reviews(db: Session = Depends(get_db)):
    reviews = db.query(Review).join(User).order_by(Review.created_at.desc()).all()
    result = []
    for review in reviews:
        result.append({
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "created_at": review.created_at.isoformat(),
            "author_id": review.author_id,
            "author_gmail": review.author.gmail
        })
    return result


async def create_review(request: Request, db: Session, text: str = Form(...), rating: int = Form(...)):
    # Получаем текущего пользователя через authx
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Необходима авторизация")

    if rating < 1 or rating > 5:
        raise HTTPException(status_code=400, detail="Рейтинг должен быть от 1 до 5")

    new_review = Review(
        text=text,
        rating=rating,
        author_id=user.id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Отзыв успешно добавлен",
            "review": {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "created_at": new_review.created_at.isoformat(),
                "author_id": new_review.author_id,
                "author_gmail": user.gmail
            }
        }
    )


async def delete_review(id: int, request: Request, db: Session):
    user = await get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Необходима авторизация")

    review = db.query(Review).filter(Review.id == id).first()
    if review is None:
        raise HTTPException(status_code=404, detail="Отзыв не найден")

    if review.author_id != user.id:
        raise HTTPException(status_code=403, detail="Вы можете удалять только свои отзывы")

    db.delete(review)
    db.commit()
    return {"message": "Отзыв удален"}
