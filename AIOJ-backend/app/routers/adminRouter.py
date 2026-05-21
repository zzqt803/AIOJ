from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.deps import require_admin
from app.models.users import User
from app.schemas.adminSchema import (
    AdminUserListResponse,
    AdminUserStatsResponse,
    AdminSubmissionListResponse,
)
import app.services.adminService as service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=AdminUserListResponse)
def get_user_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    role: str = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    from app.schemas.adminSchema import AdminUserListQuery
    query = AdminUserListQuery(
        page=page,
        page_size=page_size,
        search=search,
        role=role,
    )
    return service.get_user_list(db, query)


@router.get("/users/{user_id}/stats", response_model=AdminUserStatsResponse)
def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return service.get_user_stats(db, user_id)


@router.get("/users/{user_id}/submissions", response_model=AdminSubmissionListResponse)
def get_user_submissions(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return service.get_user_submissions(db, user_id, page, page_size)
