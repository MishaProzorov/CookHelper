from pydantic import BaseModel



class UserCreate (BaseModel):
    password: str
    gmail:str

class UserClass(BaseModel):
    id: int 
    gmail: str

    class Config:
        from_attributes = True

