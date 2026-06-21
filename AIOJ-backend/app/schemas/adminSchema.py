from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 用户列表查询
class AdminUserListQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    search: Optional[str] = None
    role: Optional[str] = None


class AdminUserListItem(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AdminUserListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[AdminUserListItem]


# 用户统计
class AdminUserStatsResponse(BaseModel):
    total_submissions: int
    accepted_submissions: int
    solved_problems: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    max_streak: int
    current_streak: int
    last_active_date: Optional[str] = None

    model_config = {"from_attributes": True}


# 用户提交记录
class AdminSubmissionItem(BaseModel):
    id: int
    problem_id: int
    language: str
    status: str
    result: Optional[str] = None
    time_used: Optional[int] = None
    memory_used: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class AdminSubmissionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[AdminSubmissionItem]


# 仪表盘统计
class AdminDashboardStatsResponse(BaseModel):
    total_users: int
    total_problems: int
    total_submissions: int
    total_problem_sets: int
    accepted_count: int
