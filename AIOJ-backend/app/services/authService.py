from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_access_token
from app.models.users import User
from app.schemas.authSchema import RegisterRequest,LoginRequest,PasswordRequest


def register(db: Session, data: RegisterRequest)->User:
    #检查用户名是否已经存在
    if db.query(User).filter(User.username == data.username).first():
        raise ValueError("用户名已存在")
    
    #检查邮箱是否已存在
    if db.query(User).filter(User.email == data.email).first():
        raise ValueError("该邮箱已被注册")
    
    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login(db: Session, data: LoginRequest)-> str:
    user = db.query(User).filter(User.email==data.email).first()

    if not user or not verify_password(data.password,user.password_hash):
        raise ValueError("邮箱或密码错误")

    return create_access_token(user.id)


def change_password(db: Session, user: User, data: PasswordRequest) -> None:
    if not verify_password(data.old_password, user.password_hash):
        raise ValueError("旧密码错误")

    user.password_hash = hash_password(data.new_password)
    db.commit()
