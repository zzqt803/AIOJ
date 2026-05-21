from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


# 用户统计
class UserStatsResponse(BaseModel):
    total_submissions: int
    accepted_submissions: int
    solved_problems: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    max_streak: int
    current_streak: int
    last_active_date: Optional[date] = None

    model_config = {"from_attributes": True}


# 排行榜
class LeaderboardItem(BaseModel):
    rank: int
    user_id: int
    username: str
    solved_problems: int
    easy_solved: int
    medium_solved: int
    hard_solved: int
    total_submissions: int
    max_streak: int
    current_streak: int


class LeaderboardResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[LeaderboardItem]
