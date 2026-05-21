from pydantic_settings import BaseSettings
from pathlib import Path
from pydantic import Field

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str

    # JWT 配置
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    ALGORITHM: str

    # 服务配置
    HOST: str
    PORT: int
    
    # redis配置
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    TASK_QUEUE: str
    RESULT_QUEUE: str
    
    class Config:
        env_file = ENV_PATH


settings = Settings()
