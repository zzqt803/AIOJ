from pydantic import BaseModel
from typing import List
from datetime import datetime


# 收藏列表
class BookmarkListItem(BaseModel):
    id: int
    problem_id: int
    title: str
    difficulty: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BookmarkListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[BookmarkListItem]


# 收藏题目
class BookmarkCreateRequest(BaseModel):
    problem_id: int


class BookmarkCreateResponse(BaseModel):
    id: int
    problem_id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# 检查是否已收藏
class BookmarkStatusResponse(BaseModel):
    is_bookmarked: bool
