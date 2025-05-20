from fastapi import Depends, HTTPException

from app.core.database import get_db
from app.services.user_service import *


def get_users(db: Session = Depends(get_db)):
    return get_all_users(db)


def get_user(user_id, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


def update_new_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    update_data = update_user(db, user, user_id)
    if not update_data:
        raise HTTPException(status_code=404, detail="User not found")
    return update_data


def remove_user(user_id, db: Session = Depends(get_db)):
    deleted = delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted
