from sqlalchemy import String, Integer, DateTime, TEXT, Boolean
from sqlalchemy import func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from datetime import datetime


class ProblemSet(Base):
    """题单"""
    __tablename__ = "problem_sets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="题单ID")

    title: Mapped[str] = mapped_column(String(100), nullable=False, comment="题单标题")

    description: Mapped[str] = mapped_column(TEXT, nullable=True, comment="题单描述")

    creator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="创建者ID"
    )

    is_public: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否公开")

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment="创建时间")

    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    items = relationship("ProblemSetItem", back_populates="problem_set", cascade="all, delete-orphan")
    creator = relationship("User")


class ProblemSetItem(Base):
    """题单-题目关联"""
    __tablename__ = "problem_set_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="关联ID")

    problem_set_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("problem_sets.id", ondelete="CASCADE"), nullable=False, comment="题单ID"
    )

    problem_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, comment="题目ID"
    )

    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序序号")

    problem_set = relationship("ProblemSet", back_populates="items")
    problem = relationship("Problem")

    __table_args__ = (
        UniqueConstraint("problem_set_id", "problem_id", name="uq_problem_set_problem"),
    )
