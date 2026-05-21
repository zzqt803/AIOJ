from sqlalchemy import Integer, DateTime, Date
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from datetime import datetime, date


class UserStats(Base):
    """用户统计"""
    __tablename__ = "user_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="统计ID")

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, comment="用户ID"
    )

    total_submissions: Mapped[int] = mapped_column(Integer, default=0, comment="总提交次数")

    accepted_submissions: Mapped[int] = mapped_column(Integer, default=0, comment="通过次数")

    solved_problems: Mapped[int] = mapped_column(Integer, default=0, comment="已解决题目数")

    easy_solved: Mapped[int] = mapped_column(Integer, default=0, comment="简单题通过数")

    medium_solved: Mapped[int] = mapped_column(Integer, default=0, comment="中等题通过数")

    hard_solved: Mapped[int] = mapped_column(Integer, default=0, comment="困难题通过数")

    max_streak: Mapped[int] = mapped_column(Integer, default=0, comment="最大连续刷题天数")

    current_streak: Mapped[int] = mapped_column(Integer, default=0, comment="当前连续刷题天数")

    last_active_date: Mapped[date] = mapped_column(Date, nullable=True, comment="最后活跃日期")

    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    user = relationship("User", back_populates="stats")
