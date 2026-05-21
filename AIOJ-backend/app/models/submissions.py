from sqlalchemy import String, Integer, DateTime, Enum, JSON, TEXT
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
import enum


class StatusEnum(enum.Enum):
    """提交状态"""
    pending = "pending"      # 等待判题
    completed = "completed"  # 判题完成


class OverallResultEnum(enum.Enum):
    """总体评测结果"""
    passed = "passed"        # 全部测试点通过
    attempted = "attempted"  # 尝试过（有测试点未通过）


class AIAnalysisStatusEnum(enum.Enum):
    """AI分析状态"""
    pending = "pending"
    analyzing = "analyzing"
    completed = "completed"


class Submission(Base):
    __tablename__ = "submissions"

    id = mapped_column(Integer, autoincrement=True, primary_key=True, comment="提交ID")

    user_id = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, comment="用户ID"
    )

    problem_id = mapped_column(
        Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, comment="题目ID"
    )

    language = mapped_column(String(20), nullable=False, comment="编程语言")

    code = mapped_column(TEXT, nullable=False, comment="代码内容")

    status = mapped_column(Enum(StatusEnum), default=StatusEnum.pending, nullable=False, comment="判题状态")

    result = mapped_column(Enum(OverallResultEnum), nullable=True, comment="总体评测结果")

    time_used = mapped_column(Integer, nullable=True, comment="总耗时（毫秒）")

    memory_used = mapped_column(Integer, nullable=True, comment="最大内存使用（KB）")

    test_case_details = mapped_column(JSON, nullable=True, comment="测试点详情")

    compile_error = mapped_column(TEXT, nullable=True, comment="编译错误信息")

    ai_analysis_status = mapped_column(
        Enum(AIAnalysisStatusEnum), default=AIAnalysisStatusEnum.pending, comment="AI分析状态"
    )

    ai_analysis_result = mapped_column(JSON, nullable=True, comment="AI分析结果")

    created_at = mapped_column(DateTime, server_default=func.now(), comment="提交时间")

    problem = relationship("Problem", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
