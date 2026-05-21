from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 获取讨论列表
class DiscussionListQuery(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)


class ReplyItem(BaseModel):
    id: int
    user_id: int
    username: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DiscussionItem(BaseModel):
    id: int
    user_id: int
    username: str
    content: str
    replies: List[ReplyItem]
    created_at: datetime

    model_config = {"from_attributes": True}


class DiscussionListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[DiscussionItem]


# 发表评论
class DiscussionCreateRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    parent_id: Optional[int] = None


class DiscussionCreateResponse(BaseModel):
    id: int
    problem_id: int
    user_id: int
    username: str
    content: str
    parent_id: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}
