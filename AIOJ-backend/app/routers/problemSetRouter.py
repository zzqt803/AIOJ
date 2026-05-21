from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.core.deps import get_current_user, require_admin
from app.models.users import User
from app.schemas.problemSetSchema import (
    ProblemSetListResponse,
    ProblemSetDetailResponse,
    ProblemSetCreateRequest,
    ProblemSetCreateResponse,
    ProblemSetUpdateRequest,
    ProblemSetItemAddRequest,
    ProblemSetItemAddResponse,
)
import app.services.problemSetService as service

router = APIRouter(prefix="/problem-sets", tags=["problem-sets"])


@router.get("", response_model=ProblemSetListResponse)
def get_problem_set_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    from app.schemas.problemSetSchema import ProblemSetListQuery
    query = ProblemSetListQuery(page=page, page_size=page_size)
    return service.get_problem_set_list(db, query)


@router.get("/{problem_set_id}", response_model=ProblemSetDetailResponse)
def get_problem_set_detail(
    problem_set_id: int,
    db: Session = Depends(get_db),
):
    try:
        return service.get_problem_set_detail(db, problem_set_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=ProblemSetCreateResponse, status_code=201)
def create_problem_set(
    data: ProblemSetCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return service.create_problem_set(db, data, current_user.id)


@router.put("/{problem_set_id}", response_model=ProblemSetCreateResponse)
def update_problem_set(
    problem_set_id: int,
    data: ProblemSetUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        return service.update_problem_set(db, problem_set_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{problem_set_id}")
def delete_problem_set(
    problem_set_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        service.delete_problem_set(db, problem_set_id)
        return {"message": "题单删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{problem_set_id}/problems", response_model=ProblemSetItemAddResponse, status_code=201)
def add_problem_to_set(
    problem_set_id: int,
    data: ProblemSetItemAddRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        return service.add_problem_to_set(db, problem_set_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{problem_set_id}/problems/{problem_id}")
def remove_problem_from_set(
    problem_set_id: int,
    problem_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    try:
        service.remove_problem_from_set(db, problem_set_id, problem_id)
        return {"message": "题目已从题单移除"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
