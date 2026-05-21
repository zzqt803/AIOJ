from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.submissions import AIAnalysisStatusEnum


# 提交代码
class SubmitCodeRequest(BaseModel):
    problem_id: int
    language: str = Field(..., pattern="^(cpp|c|java|python)$")
    code: str = Field(..., min_length=1, max_length=65536)


class SubmitCodeResponse(BaseModel):
    id: int
    problem_id: int
    language: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# 单个测试点结果
class TestCaseResult(BaseModel):
    test_case_id: int
    status: str  # accepted, wrong_answer, runtime_error, time_limit, memory_limit, compile_error, system_error
    time_used_ms: int
    memory_used_kb: int
    error_message: Optional[str] = ""


# 获取提交列表
class SubmissionListQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    problem_id: Optional[int] = None
    status: Optional[str] = None
    language: Optional[str] = None


class SubmissionListItem(BaseModel):
    id: int
    problem_id: int
    language: str
    status: str  # pending, completed
    result: Optional[str] = None  # passed, attempted
    time_used: Optional[int] = None  # 毫秒
    memory_used: Optional[int] = None  # KB
    created_at: datetime

    model_config = {"from_attributes": True}


class SubmissionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[SubmissionListItem]


# 获取提交详情
class SubmissionDetailResponse(BaseModel):
    id: int
    problem_id: int
    user_id: int
    language: str
    code: str
    status: str  # pending, completed
    result: Optional[str] = None  # passed, attempted
    time_used: Optional[int] = None  # 毫秒
    memory_used: Optional[int] = None  # KB
    test_case_details: Optional[List[TestCaseResult]] = None
    compile_error: Optional[str] = None
    ai_analysis_status: AIAnalysisStatusEnum
    created_at: datetime

    model_config = {"from_attributes": True}


# 获取AI分析结果
class CodeIssue(BaseModel):
    line: Optional[int] = None
    description: str


class AIAnalysisResult(BaseModel):
    summary: str
    time_complexity: str
    space_complexity: str
    issues: List[CodeIssue]
    suggestions: List[str]
    score: int


class AIAnalysisResultResponse(BaseModel):
    submission_id: int
    ai_analysis_status: AIAnalysisStatusEnum
    ai_analysis_result: Optional[AIAnalysisResult] = None


