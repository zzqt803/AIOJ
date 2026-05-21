from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.db.deps import get_db
from app.core.deps import get_current_user, require_admin
from app.models.users import User
from app.schemas.problemSchema import (
    ProblemListResponse,
    ProblemListQuery,
    ProblemDetailResponse,
    ProblemCreateRequest,
    ProblemUpdateRequest,
    ProblemCreateResponse,
)
import app.services.problemService as service

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("", response_model=ProblemListResponse)
def get_problem_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    difficulty: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = ProblemListQuery(
        page=page,
        page_size=page_size,
        difficulty=difficulty,
        tag=tag,
    )
    return service.get_problem_list(db, query)


@router.get("/{problem_id}", response_model=ProblemDetailResponse)
def get_problem_detail(
    problem_id: int,
    db: Session = Depends(get_db),
):
    try:
        problem = service.get_problem_detail(db, problem_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return problem


@router.post("", response_model=ProblemCreateResponse, status_code=201)
def create_problem(
    data: ProblemCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return service.create_problem(db, data)


@router.put("/{problem_id}", response_model=ProblemCreateResponse)
def update_problem(
    problem_id: int,
    data: ProblemUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        return service.update_problem(db, problem_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete("/{problem_id}")
def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        service.delete_problem(db, problem_id)
        return {"message": "题目删除成功"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )