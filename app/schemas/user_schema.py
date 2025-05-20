from pydantic import BaseModel, EmailStr
from typing import List
from app.schemas.contact_schema import ContactResponse

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    contacts: List[ContactResponse] = []

    class Config:
        from_attributes = True