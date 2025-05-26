from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core.auth import hash_password
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.utils.response_paginated import response_paginated


class UserService:
    def create(self, db: Session, user_in: UserCreate):
        try:
            # Check for duplicate email or username
            if db.query(User).filter(User.email == user_in.email).first():
                return {
                    "success": False,
                    "message": "The given data was invalid",
                    "errors": {"email": ["Email already registered."]}
                }
            if db.query(User).filter(User.username == user_in.username).first():
                return {
                    "success": False,
                    "message": "The given data was invalid",
                    "errors": {"username": ["Username already taken."]}
                }
            bcrypt_password_hash = hash_password(user_in.password_hash)
            user = User(
                username=user_in.username,
                email=user_in.email,
                password_hash=bcrypt_password_hash,
                full_name=user_in.full_name,
                profile_picture=user_in.profile_picture,
                bio=user_in.bio,
                created_at=datetime.now()
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

    def edit(self, db: Session, user_id: int):
        try:
            user = db.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found."}
            return {"success": True, "data": user}
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Database error: {str(e)}"}

    def update(self, db: Session, user_id: int, user_in: UserUpdate):
        try:
            user = db.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found."}

            for field, value in user_in.dict(exclude_unset=True).items():
                setattr(user, field, value)
            db.commit()
            db.refresh(user)
            return {"success": True, "message": "User updated.", "data": user}
        except SQLAlchemyError as e:
            db.rollback()
            return {"success": False, "message": f"Database error: {str(e)}"}

    def delete(self, db: Session, user_id: int):
        try:
            user = db.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found."}
            db.delete(user)
            db.commit()
            return {"success": True, "message": "User deleted."}
        except SQLAlchemyError as e:
            db.rollback()
            return {"success": False, "message": f"Database error: {str(e)}"}

    def index(self, db: Session, page: int = 1, limit: int = 10):
        try:
            offset = (page - 1) * limit
            query = db.query(User).options(joinedload(User.addresses))
            total = query.count()
            users = query.offset(offset).limit(limit).all()
            return response_paginated(data=users, total=total, page=page, limit=limit)
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Database error: {str(e)}"}


user_service = UserService()
