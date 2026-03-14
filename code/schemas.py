from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    gmail: EmailStr


class UserCreate (UserBase):
    password: str
    
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None

class UserClass(UserBase):
    id: int 
    name: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        from_attributes = True

