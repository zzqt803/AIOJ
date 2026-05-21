from app.db.redis import redis_client
from app.core.config import settings
import json
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.schemas.submissionSchema import(
    SubmitCodeRequest,SubmitCodeResponse,
    AIAnalysisStatusEnum,AIAnalysisResultResponse,
    SubmissionListQuery,SubmissionListResponse,SubmissionListItem,
    SubmissionDetailResponse
)
from app.models.users import User
from app.models.submissions import Submission ,StatusEnum
from app.models.problems import Problem
from datetime import datetime

def submit_code(db: Session,data: SubmitCodeRequest,current_user: User)->SubmitCodeResponse:
    # 保存提交记录到数据库
    submission = Submission(
        user_id = current_user.id,
        problem_id = data.problem_id,
        language=data.language,
        code=data.code,
        status=StatusEnum.pending,
        ai_analysis_status=AIAnalysisStatusEnum.pending,
        created_at=datetime.now()
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    # 获取题目信息
    problem = db.query(Problem).filter(Problem.id == data.problem_id).first()
    if not problem:
        raise ValueError("题目不存在")

    # 构建判题任务
    judge_task = {
        "submission_id": str(submission.id),
        "problem_id": str(data.problem_id),
        "language": data.language,
        "source_code": data.code,
        "time_limit_ms": problem.time_limit,  # 已经是毫秒
        "memory_limit_kb": problem.memory_limit * 1024  # MB转KB
    }

    # 推入Redis任务队列
    redis_client.lpush(settings.TASK_QUEUE, json.dumps(judge_task))

    return SubmitCodeResponse.model_validate(submission)


def get_submission_list(db: Session,query: SubmissionListQuery,current_user: User)->SubmissionListResponse:
    stmt = db.query(Submission).filter(Submission.user_id==current_user.id)

    if query.problem_id:
        stmt = stmt.filter(Submission.problem_id == query.problem_id)
    if query.status:
        stmt = stmt.filter(Submission.status == query.status)
    if query.language:
        stmt = stmt.filter(Submission.language == query.language)

    total = stmt.with_entities(func.count()).scalar()
    items = (
        stmt.order_by(Submission.created_at.desc())
        .offset((query.page - 1) * query.page_size)
        .limit(query.page_size)
        .all()
    )

    return SubmissionListResponse(
        total=total,
        page=query.page,
        page_size=query.page_size,
        items=[SubmissionListItem.model_validate(item) for item in items],
    )

def get_submission_detail(db: Session,submission_id: int,current_user: User)->SubmissionDetailResponse:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise ValueError("提交记录不存在")
    if submission.user_id != current_user.id:
        raise ValueError("提交记录不存在")
    return SubmissionDetailResponse.model_validate(submission)


def get_ai_analysis(db: Session, submission_id: int, current_user: User) -> AIAnalysisResultResponse:
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if not submission:
        raise ValueError("提交记录不存在")
    if submission.user_id != current_user.id:
        raise ValueError("提交记录不存在")

    return AIAnalysisResultResponse(
        submission_id=submission.id,
        ai_analysis_status=submission.ai_analysis_status,
        ai_analysis_result=submission.ai_analysis_result
    )
