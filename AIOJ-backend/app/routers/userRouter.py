from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.models.users import User
from app.schemas.userSchema import UserInfoResponse
import app.services.userService as service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserInfoResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    return service.get_user_info(current_user)
