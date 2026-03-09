from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    hashed_password = Column(String)
    gmail = Column(String, unique=True, index=True)

 