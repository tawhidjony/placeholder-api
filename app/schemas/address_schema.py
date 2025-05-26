from pydantic import BaseModel


class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class AddressCreate(AddressBase):
    user_id: int


class AddressOut(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
