from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.deps import get_current_user
from app.models.users import User, RoleEnum
from app.schemas.discussionSchema import (
    DiscussionListResponse,
    DiscussionCreateRequest,
    DiscussionCreateResponse,
)
import app.services.discussionService as service

router = APIRouter(tags=["discussions"])


@router.get("/problems/{problem_id}/discussions", response_model=DiscussionListResponse)
def get_discussion_list(
    problem_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    from app.schemas.discussionSchema import DiscussionListQuery
    query = DiscussionListQuery(page=page, page_size=page_size)
    return service.get_discussion_list(db, problem_id, query)


@router.post("/problems/{problem_id}/discussions", response_model=DiscussionCreateResponse, status_code=201)
def create_discussion(
    problem_id: int,
    data: DiscussionCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.create_discussion(db, problem_id, data, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/discussions/{discussion_id}")
def delete_discussion(
    discussion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        is_admin = current_user.role == RoleEnum.admin
        service.delete_discussion(db, discussion_id, current_user.id, is_admin)
        return {"message": "评论已删除"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
