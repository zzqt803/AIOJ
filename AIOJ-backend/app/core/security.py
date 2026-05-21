from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from app.core.config import settings

load_dotenv()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# 密码哈希
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# 验证密码
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# 生成 JWT
def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={"sub": str(user_id),"exp":expire}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

# 解析 JWT
def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return int(payload["sub"])

    
