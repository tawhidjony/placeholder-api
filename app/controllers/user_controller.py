from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.services.user_service import user_service

route = APIRouter()


@route.get("/users", response_model=List[UserOut])
def all_list_users(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    result = user_service.index(db=db, page=page, limit=limit)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    return result


@route.post("/users")
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    result = user_service.create(db, user_in)
    if not result["success"]:
        raise HTTPException(
            status_code=422 if "errors" in result else 400,
            detail={
                "message": result.get("message", "An error occurred"),
                "errors": result.get("errors")
            } if "errors" in result else result.get("message", "Unknown error")
        )
    return result


@route.get("/users/{user_id}")
def edit_user(user_id: int, db: Session = Depends(get_db)):
    result = user_service.edit(db, user_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@route.put("/users/{user_id}")
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    result = user_service.update(db, user_id, user_in)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result


@route.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    result = user_service.delete(db, user_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return result
