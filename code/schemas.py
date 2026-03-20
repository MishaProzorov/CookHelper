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

# class UserClass(UserBase):
#     id: int 
#     name: Optional[str] = None
#     phone: Optional[str] = None

#     class Config:
#         from_attributes = True

