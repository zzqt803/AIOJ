from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.users import User
from app.models.user_stats import UserStats
from app.models.submissions import Submission
from app.schemas.adminSchema import (
    AdminUserListQuery,
    AdminUserListResponse,
    AdminUserListItem,
    AdminUserStatsResponse,
    AdminSubmissionListResponse,
    AdminSubmissionItem,
)


def get_user_list(db: Session, query: AdminUserListQuery) -> AdminUserListResponse:
    stmt = db.query(User)

    # 搜索
    if query.search:
        search_term = f"%{query.search}%"
        stmt = stmt.filter(
            or_(
                User.username.ilike(search_term),
                User.email.ilike(search_term),
            )
        )

    # 角色筛选
    if query.role:
        stmt = stmt.filter(User.role == query.role)

    total = stmt.count()

    items = stmt.order_by(User.created_at.desc()).offset(
        (query.page - 1) * query.page_size
    ).limit(query.page_size).all()

    return AdminUserListResponse(
        total=total,
        page=query.page,
        page_size=query.page_size,
        items=[AdminUserListItem.model_validate(item) for item in items],
    )


def get_user_stats(db: Session, user_id: int) -> AdminUserStatsResponse:
    stats = db.query(UserStats).filter(UserStats.user_id == user_id).first()
    if not stats:
        return AdminUserStatsResponse(
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
    return AdminUserStatsResponse(
        total_submissions=stats.total_submissions,
        accepted_submissions=stats.accepted_submissions,
        solved_problems=stats.solved_problems,
        easy_solved=stats.easy_solved,
        medium_solved=stats.medium_solved,
        hard_solved=stats.hard_solved,
        max_streak=stats.max_streak,
        current_streak=stats.current_streak,
        last_active_date=str(stats.last_active_date) if stats.last_active_date else None,
    )


def get_user_submissions(db: Session, user_id: int, page: int = 1, page_size: int = 20) -> AdminSubmissionListResponse:
    stmt = db.query(Submission).filter(Submission.user_id == user_id)

    total = stmt.count()

    items = stmt.order_by(Submission.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    return AdminSubmissionListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[AdminSubmissionItem.model_validate(item) for item in items],
    )
