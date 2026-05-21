from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 获取题目列表
class ProblemListQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    difficulty: Optional[str] = None
    tag: Optional[str] = None


class ProblemListItem(BaseModel):
    id: int
    title: str
    difficulty: str
    tags: List[str]
    time_limit: int  # 毫秒
    memory_limit: int  # MB

    model_config = {"from_attributes": True}


class ProblemListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ProblemListItem]


# 获取题目详情
class ProblemDetailResponse(BaseModel):
    id: int
    title: str
    difficulty: str
    tags: List[str]
    description: str
    input_format: str
    output_format: str
    sample_input: str
    sample_output: str
    hint: Optional[str] = None
    time_limit: int  # 毫秒
    memory_limit: int  # MB
    created_at: datetime

    model_config = {"from_attributes": True}


# 创建题目
class ProblemCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    difficulty: str = Field("easy", pattern="^(easy|medium|hard)$")
    tags: List[str] = []
    description: str
    input_format: str
    output_format: str
    sample_input: str
    sample_output: str
    hint: Optional[str] = None
    time_limit: int = Field(1000, ge=100, le=10000)
    memory_limit: int = Field(256, ge=16, le=1024)
    is_public: bool = True


class ProblemCreateResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


# 更新题目
class ProblemUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")
    tags: Optional[List[str]] = None
    description: Optional[str] = None
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    sample_input: Optional[str] = None
    sample_output: Optional[str] = None
    hint: Optional[str] = None
    time_limit: Optional[int] = Field(None, ge=100, le=10000)
    memory_limit: Optional[int] = Field(None, ge=16, le=1024)
    is_public: Optional[bool] = None