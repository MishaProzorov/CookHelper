from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate (BaseModel):
    password: str
    gmail:str

class UserClass(BaseModel):
    id: int
    gmail: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None

class RecipePreview(BaseModel):
    id: int
    title: str
    image: Optional[str] = None

class RecipeFull(RecipePreview):
    ingredients: str  # Все ингредиенты одной строкой
    instructions: Optional[str] = None # Текст инструкции