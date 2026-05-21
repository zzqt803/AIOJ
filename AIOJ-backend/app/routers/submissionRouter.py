from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.db.deps import get_db
from app.core.deps import get_current_user
from app.models.users import User
from app.models.submissions import AIAnalysisStatusEnum
from app.schemas.submissionSchema import (
    SubmitCodeRequest,
    SubmitCodeResponse,
    SubmissionListQuery,
    SubmissionListResponse,
    SubmissionDetailResponse,
    AIAnalysisResultResponse,
)
import app.services.submissionService as service

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.post("", response_model=SubmitCodeResponse, status_code=201)
def submit_code(
    data: SubmitCodeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    submission = service.submit_code(db, data, current_user)
    return submission


@router.get("", response_model=SubmissionListResponse)
def get_submission_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    problem_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = SubmissionListQuery(
        page=page,
        page_size=page_size,
        problem_id=problem_id,
        status=status,
        language=language,
    )
    return service.get_submission_list(db, query, current_user)


@router.get("/{submission_id}", response_model=SubmissionDetailResponse)
def get_submission_detail(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_submission_detail(db, submission_id, current_user)


@router.get("/{submission_id}/ai-analysis", response_model=AIAnalysisResultResponse)
def get_ai_analysis(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.get_ai_analysis(db, submission_id, current_user)
