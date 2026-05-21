from sqlalchemy import String, Integer, DateTime, Enum, JSON, TEXT, Boolean
from sqlalchemy import func
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.db.base import Base
import enum


class DifficultyEnum(enum.Enum):
    """题目难度"""
    easy = "easy"
    medium = "medium"
    hard = "hard"


class Problem(Base):
    __tablename__ = "problems"

    id = mapped_column(Integer, primary_key=True, autoincrement=True, comment="题目ID")

    title = mapped_column(String(100), nullable=False, comment="题目标题")

    difficulty = mapped_column(Enum(DifficultyEnum), default=DifficultyEnum.easy, comment="题目难度")

    tags = mapped_column(JSON, nullable=False, default=list, comment="题目标签列表")

    description = mapped_column(TEXT, nullable=False, comment="题目描述")

    input_format = mapped_column(TEXT, nullable=False, comment="输入格式说明")

    output_format = mapped_column(TEXT, nullable=False, comment="输出格式说明")

    sample_input = mapped_column(TEXT, nullable=False, comment="样例输入")

    sample_output = mapped_column(TEXT, nullable=False, comment="样例输出")

    hint = mapped_column(TEXT, nullable=True, comment="提示/解题思路")

    time_limit = mapped_column(Integer, default=1000, comment="时间限制（毫秒）")

    memory_limit = mapped_column(Integer, default=256, comment="内存限制（MB）")

    is_public = mapped_column(Boolean, default=True, comment="是否公开")

    created_at = mapped_column(DateTime, server_default=func.now(), comment="创建时间")

    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    submissions = relationship("Submission", back_populates="problem")
    discussions = relationship("Discussion", back_populates="problem")
    bookmarks = relationship("Bookmark", back_populates="problem")
