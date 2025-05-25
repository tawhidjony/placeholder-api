from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    username: str = Field(..., example="admin")
    email: EmailStr = Field(..., example="admin@admin.com")
    password_hash: str = Field(..., example="admin")


class UserLogin(BaseModel):
    username: str = Field(..., example="admin")
    password_hash: str = Field(..., example="admin")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
