from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.deps import get_current_user
from app.models.users import User
from app.schemas.statsSchema import UserStatsResponse, LeaderboardResponse
import app.services.statsService as service

router = APIRouter(tags=["stats"])


@router.get("/users/me/stats", response_model=UserStatsResponse)
def get_current_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_user_stats(db, current_user.id)


@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.get_leaderboard(db, page, page_size)
