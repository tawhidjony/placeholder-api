from fastapi import APIRouter

from app.controllers import (
    user_controller,
)
from app.controllers.auth import (
    auth_controller,
)

router = APIRouter()

router.include_router(auth_controller.route, prefix="/auth", tags=["Authentication"])
router.include_router(user_controller.route, prefix="/users", tags=["users"])
