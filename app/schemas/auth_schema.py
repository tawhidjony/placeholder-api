from pydantic import BaseModel, Field
from typing_extensions import Annotated
from pydantic import EmailStr

class UserRegister(BaseModel):
    username: Annotated[str, Field(example="admin")]
    email: Annotated[EmailStr, Field(example="admin@admin.com")]
    password_hash: Annotated[str, Field(example="admin")]


class UserLogin(BaseModel):
    username: Annotated[str ,Field(example="admin")]
    password_hash: Annotated[str ,Field(example="admin")]


class Token(BaseModel):
    access_token:str
    token_type:str = "bearer"
