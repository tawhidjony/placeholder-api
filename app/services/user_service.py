from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models.user_model import User


def all_users(db: Session, skip: int = 0, limit: int = 10) -> Tuple[int, List[User]]:
    total = db.query(User).count()
    users = db.query(User).offset(skip).limit(limit).all()
    return total, users
