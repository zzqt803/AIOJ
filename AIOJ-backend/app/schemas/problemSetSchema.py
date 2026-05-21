from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 获取题单列表
class ProblemSetListQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class ProblemSetListItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    creator_name: str
    problem_count: int
    is_public: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ProblemSetListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ProblemSetListItem]


# 获取题单详情
class ProblemInSet(BaseModel):
    problem_id: int
    title: str
    difficulty: str
    sort_order: int


class ProblemSetDetailResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    creator_id: int
    creator_name: str
    is_public: bool
    problems: List[ProblemInSet]
    created_at: datetime

    model_config = {"from_attributes": True}


# 创建题单
class ProblemSetCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: bool = True


class ProblemSetCreateResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


# 更新题单
class ProblemSetUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_public: Optional[bool] = None


# 添加题目到题单
class ProblemSetItemAddRequest(BaseModel):
    problem_id: int
    sort_order: int = 0


class ProblemSetItemAddResponse(BaseModel):
    id: int
    problem_set_id: int
    problem_id: int
    sort_order: int

    model_config = {"from_attributes": True}
