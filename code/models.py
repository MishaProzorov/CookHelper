from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    password = Column(String, index=True)
    gmail = Column(String, index=True)

 