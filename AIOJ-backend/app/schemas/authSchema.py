from pydantic import BaseModel,EmailStr, field_validator
import re

# -------- 注册 --------
class RegisterRequest(BaseModel):
    username:str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v:str)->str:
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", v):
            raise ValueError("用户名只能包含字母、数字、下划线，长度 3-20")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("密码长度至少 8 位")
        return v


class RegisterResponse(BaseModel):
    id: int
    username: str
    email: str

# -------- 登录 --------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# -------- 密码 --------
class PasswordRequest(BaseModel):

    old_password: str
    new_password: str
    confirm_password: str
    
    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        if "new_password" in info.data and v != info.data["new_password"]:
            raise ValueError("两次密码不一致")
        return v

class PasswordResponse(BaseModel):
    message: str

