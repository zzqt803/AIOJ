from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.bookmark import Bookmark
from app.models.problems import Problem
from app.schemas.bookmarkSchema import (
    BookmarkListResponse,
    BookmarkListItem,
    BookmarkCreateRequest,
    BookmarkCreateResponse,
    BookmarkStatusResponse,
)


def get_bookmark_list(db: Session, user_id: int, page: int = 1, page_size: int = 20) -> BookmarkListResponse:
    stmt = (
        db.query(
            Bookmark.id,
            Bookmark.problem_id,
            Bookmark.created_at,
            Problem.title,
            Problem.difficulty,
        )
        .join(Problem, Problem.id == Bookmark.problem_id)
        .filter(Bookmark.user_id == user_id)
        .order_by(Bookmark.created_at.desc())
    )

    total = db.query(func.count(Bookmark.id)).filter(Bookmark.user_id == user_id).scalar()

    items = stmt.offset((page - 1) * page_size).limit(page_size).all()

    return BookmarkListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[BookmarkListItem.model_validate(item) for item in items],
    )


def create_bookmark(db: Session, user_id: int, data: BookmarkCreateRequest) -> BookmarkCreateResponse:
    # 检查题目是否存在
    problem = db.query(Problem).filter(Problem.id == data.problem_id).first()
    if not problem:
        raise ValueError("题目不存在")

    # 检查是否已收藏
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.problem_id == data.problem_id,
    ).first()
    if existing:
        raise ValueError("已收藏该题目")

    bookmark = Bookmark(
        user_id=user_id,
        problem_id=data.problem_id,
    )
    db.add(bookmark)
    db.commit()
    db.refresh(bookmark)
    return BookmarkCreateResponse.model_validate(bookmark)


def delete_bookmark(db: Session, user_id: int, problem_id: int) -> None:
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.problem_id == problem_id,
    ).first()
    if not bookmark:
        raise ValueError("未收藏该题目")
    db.delete(bookmark)
    db.commit()


def check_bookmark_status(db: Session, user_id: int, problem_id: int) -> BookmarkStatusResponse:
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.problem_id == problem_id,
    ).first()
    return BookmarkStatusResponse(is_bookmarked=bookmark is not None)
