from typing import List

from fastapi import APIRouter

from app.controllers import user_controller
from app.schemas.user_schema import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

router.get("/", response_model=List[UserResponse])(user_controller.get_users)
router.get("/{user_id}", response_model=UserResponse)(user_controller.get_user)
router.post("/", response_model=UserResponse)(user_controller.create_new_user)
router.put("/{user_id}", response_model=UserResponse)(user_controller.update_new_user)
router.delete("/{user_id}", response_model=UserResponse)(user_controller.remove_user)
