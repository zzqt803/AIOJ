from sqlalchemy import Integer, DateTime
from sqlalchemy import func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from datetime import datetime


class Bookmark(Base):
    """题目收藏"""
    __tablename__ = "bookmarks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID"
    )

    problem_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, comment="题目ID"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="收藏时间")

    user = relationship("User", back_populates="bookmarks")
    problem = relationship("Problem", back_populates="bookmarks")

    __table_args__ = (
        UniqueConstraint("user_id", "problem_id", name="uq_user_problem_bookmark"),
    )
