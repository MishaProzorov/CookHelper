from sqlalchemy import Column, Integer, String, Text
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    hashed_password = Column(String)
    gmail = Column(String, unique=True, index=True)


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