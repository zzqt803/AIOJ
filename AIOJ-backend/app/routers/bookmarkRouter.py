from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.deps import get_current_user
from app.models.users import User
from app.schemas.bookmarkSchema import (
    BookmarkListResponse,
    BookmarkCreateRequest,
    BookmarkCreateResponse,
    BookmarkStatusResponse,
)
import app.services.bookmarkService as service

router = APIRouter(tags=["bookmarks"])


@router.get("/bookmarks", response_model=BookmarkListResponse)
def get_bookmark_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_bookmark_list(db, current_user.id, page, page_size)


@router.post("/bookmarks", response_model=BookmarkCreateResponse, status_code=201)
def create_bookmark(
    data: BookmarkCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return service.create_bookmark(db, current_user.id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/bookmarks/{problem_id}")
def delete_bookmark(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        service.delete_bookmark(db, current_user.id, problem_id)
        return {"message": "已取消收藏"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/problems/{problem_id}/is-bookmarked", response_model=BookmarkStatusResponse)
def check_bookmark_status(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.check_bookmark_status(db, current_user.id, problem_id)
