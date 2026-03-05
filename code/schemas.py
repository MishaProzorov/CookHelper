from pydantic import BaseModel



class UserBase (BaseModel):
    name: str
    age: int 
    password: str
    gmail:str

class UserClass(UserBase):
    id: int 

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass