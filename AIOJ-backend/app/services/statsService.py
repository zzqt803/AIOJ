from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user_stats import UserStats
from app.models.users import User
from app.schemas.statsSchema import (
    UserStatsResponse,
    LeaderboardItem,
    LeaderboardResponse,
)


def get_user_stats(db: Session, user_id: int) -> UserStatsResponse:
    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    if not stats:
        # 如果没有统计记录，返回默认值
        return UserStatsResponse(
            total_submissions=0,
            accepted_submissions=0,
            solved_problems=0,
            easy_solved=0,
            medium_solved=0,
            hard_solved=0,
            max_streak=0,
            current_streak=0,
            last_active_date=None,
        )
    return UserStatsResponse.model_validate(stats)


def get_leaderboard(db: Session, page: int = 1, page_size: int = 20) -> LeaderboardResponse:
    # 查询排行榜
    stmt = (
        db.query(
            User.id.label("user_id"),
            User.username,
            UserStats.solved_problems,
            UserStats.easy_solved,
            UserStats.medium_solved,
            UserStats.hard_solved,
            UserStats.total_submissions,
            UserStats.max_streak,
            UserStats.current_streak,
        )
        .join(UserStats, UserStats.user_id == User.id)
        .filter(User.is_active == True, User.role == "user")
        .order_by(UserStats.solved_problems.desc(), UserStats.accepted_submissions.asc())
    )

    total = db.query(func.count(User.id)).join(UserStats).filter(
        User.is_active == True, User.role == "user"
    ).scalar()

    items = stmt.offset((page - 1) * page_size).limit(page_size).all()

    leaderboard_items = []
    for i, item in enumerate(items):
        leaderboard_items.append(LeaderboardItem(
            rank=(page - 1) * page_size + i + 1,
            user_id=item.user_id,
            username=item.username,
            solved_problems=item.solved_problems,
            easy_solved=item.easy_solved,
            medium_solved=item.medium_solved,
            hard_solved=item.hard_solved,
            total_submissions=item.total_submissions,
            max_streak=item.max_streak,
            current_streak=item.current_streak,
        ))

    return LeaderboardResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=leaderboard_items,
    )
