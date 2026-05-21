from sqlalchemy import Integer, String, DateTime, Boolean, Enum
from sqlalchemy import func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from datetime import datetime
import enum


class RoleEnum(str, enum.Enum):
    """用户角色"""
    admin = "admin"    # 管理员，可管理题目
    user = "user"      # 普通用户，可刷题提交
    guest = "guest"    # 游客，只能浏览


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")

    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, comment="邮箱")

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码哈希")

    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.user, nullable=False, comment="用户角色")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否启用")

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")

    submissions = relationship("Submission", back_populates="user")
    stats = relationship("UserStats", back_populates="user", uselist=False)
    discussions = relationship("Discussion", back_populates="user")
    bookmarks = relationship("Bookmark", back_populates="user")
