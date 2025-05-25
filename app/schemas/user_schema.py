from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., example="mahmud123")
    email: EmailStr = Field(..., example="mahmud@example.com")
    full_name: str | None = Field(None, example="Mahmud Hasan")
    profile_picture: str | None = Field(None, example="https://example.com/image.jpg ")
    bio: str | None = Field(None, example="আমি একজন সফটওয়্যার ডেভেলপার।")


class UserCreate(UserBase):
    password_hash: str = Field(..., example="hashedpassword123")

    @classmethod
    def validate_fields(cls, values):
        required_fields = {
            'username': values.get('username'),
            'email': values.get('email'),
            'password_hash': values.get('password_hash')
        }

        errors = {}
        for field, value in required_fields.items():
            if not value or value.strip() == "":
                errors[field] = ["The field is required."]

        if errors:
            raise ValueError("Required fields missing", errors)

        return values


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, example="নতুন নাম")
    profile_picture: str | None = Field(None, example="https://example.com/new-image.jpg ")
    bio: str | None = Field(None, example="নতুন বায়ো")
    is_active: bool | None = Field(None, example=True)
