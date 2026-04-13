from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    hashed_password = Column(String)
    gmail = Column(String, unique=True, index=True)

    reviews = relationship("Review", back_populates="author")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="reviews")



class RecipeCache(Base):
    __tablename__ = "recipe_cache"
    id = Column(Integer, primary_key=True) # ID от Spoonacular
    title_ru = Column(String)
    title_en = Column(String)
    image = Column(String, nullable=True)
    ingredients_ru = Column(Text, nullable=True)
    ingredients_en = Column(Text, nullable=True)
    instructions_ru = Column(Text, nullable=True)
    instructions_en = Column(Text, nullable=True)