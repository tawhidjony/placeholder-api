from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate


class CRUDUser:
    def create_user(self, db: Session, user_in: UserCreate):
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
            hashed_password = hash_password(user_in.password_hash)
            user = User(
                username=user_in.username,
                email=user_in.email,
                password_hash=hashed_password,
                full_name=user_in.full_name,
                profile_picture=user_in.profile_picture,
                bio=user_in.bio,
                created_at=datetime.utcnow()
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

    def get_user(self, db: Session, user_id: int):
        try:
            user = db.query(User).get(user_id)
            if not user:
                return {"success": False, "message": "User not found."}
            return {"success": True, "data": user}
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Database error: {str(e)}"}

    def update_user(self, db: Session, user_id: int, user_in: UserUpdate):
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

    def delete_user(self, db: Session, user_id: int):
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

    def list_users(self, db: Session, page: int = 1, limit: int = 10):
        try:
            offset = (page - 1) * limit
            query = db.query(User)
            total = query.count()
            users = query.offset(offset).limit(limit).all()
            return {
                "success": True,
                "message": "User list fetched successfully.",
                "data": users,
                "pagination": {
                    "total": total,
                    "page": page,
                    "limit": limit,
                    "pages": (total + limit - 1) // limit,
                    "has_next": offset + limit < total,
                    "has_prev": page > 1
                }
            }
        except SQLAlchemyError as e:
            return {"success": False, "message": f"Database error: {str(e)}"}


crud_user = CRUDUser()
