from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth_schema import UserRegister, UserLogin, Token
from app.services.auth_service import auth_service

route = APIRouter()


@route.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    result = auth_service.register(db, user)
    if not result["success"]:
        raise HTTPException(
            status_code=422 if "errors" in result else 400,
            detail={
                "message": result.get("message", "An error occurred"),
                "errors": result.get("errors")
            } if "errors" in result else result.get("message", "Unknown error")
        )
    return result


@route.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login(db, user)
