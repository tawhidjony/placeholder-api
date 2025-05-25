from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.core.auth import verify_password, create_access_token
from app.core.security import hash_password
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserLogin


class AuthService:
    def register(self, db: Session, schema: UserRegister):
        try:
            if db.query(User).filter(User.email == schema.email).first():
                return {
                    "success": False,
                    "message": "The given data was invalid",
                    "errors": {"email": ["Email already registered."]}
                }
            if db.query(User).filter(User.username == schema.username).first():
                return {
                    "success": False,
                    "message": "The given data was invalid",
                    "errors": {"username": ["Username already taken."]}
                }
            hashed_password = hash_password(schema.password_hash)
            user = User(
                username=schema.username,
                email=schema.email,
                password_hash=hashed_password,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return {"success": True, "message": "User created successfully.", "data": user}

        except IntegrityError:
            db.rollback()
            return {
                "success": False,
                "message": "The given data was invalid",
                "errors": {"database": ["Integrity error. Possibly duplicate entry."]}
            }
        except SQLAlchemyError as e:
            db.rollback()
            return {
                "success": False,
                "message": "The given data was invalid",
                "errors": {"database": [f"Database error: {str(e)}"]}
            }

    def login(self, db: Session, schema: UserLogin):
        user = db.query(User).filter(User.username == schema.username).first()
        if not user or not verify_password(schema.password_hash, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
        return {"access_token": token, "token_type": "bearer"}


auth_service = AuthService()
