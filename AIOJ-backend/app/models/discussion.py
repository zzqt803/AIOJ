from sqlalchemy import Integer, DateTime, TEXT
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from datetime import datetime


class Discussion(Base):
    """题目讨论"""
    __tablename__ = "discussions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="评论ID")

    problem_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, comment="题目ID"
    )

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID"
    )

    content: Mapped[str] = mapped_column(TEXT, nullable=False, comment="评论内容")

    parent_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("discussions.id", ondelete="CASCADE"), nullable=True, comment="父评论ID，NULL为顶级评论"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")

    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    problem = relationship("Problem")
    user = relationship("User", back_populates="discussions")
    replies = relationship("Discussion", backref="parent", remote_side=[id])
