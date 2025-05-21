from fastapi import APIRouter

from app.controllers import (user_controller)

router = APIRouter()

router.include_router(user_controller.route, prefix="/users", tags=["users"])
