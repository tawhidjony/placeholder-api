from pydantic import BaseModel, EmailStr

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    phone: str

class ContactCreate(ContactBase):
    user_id: int

class ContactUpdate(ContactBase):
    user_id: int

class ContactResponse(ContactBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True