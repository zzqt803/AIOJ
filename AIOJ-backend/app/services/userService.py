from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.userSchema import UserInfoResponse


def get_user_info(user: User) -> UserInfoResponse:
    return UserInfoResponse.model_validate(user)
