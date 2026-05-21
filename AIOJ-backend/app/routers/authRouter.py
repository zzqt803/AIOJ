from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.authSchema import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    PasswordRequest,
    PasswordResponse,
)
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.deps import get_current_user
import app.services.authService as service
from app.models.users import User


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED
)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    try:
        user = service.register(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return RegisterResponse(id=user.id, username=user.username, email=user.email)


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = service.login(db, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return LoginResponse(access_token=token)


@router.post("/password", response_model=PasswordResponse)
def change_password(
    data: PasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        service.change_password(db, current_user, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return PasswordResponse(message="密码修改成功")
