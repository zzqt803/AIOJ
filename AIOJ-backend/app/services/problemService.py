from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.problems import Problem
from app.schemas.problemSchema import (
    ProblemListQuery,
    ProblemListResponse,
    ProblemDetailResponse,
    ProblemListItem,
    ProblemCreateRequest,
    ProblemUpdateRequest,
    ProblemCreateResponse,
)
from datetime import datetime


def get_problem_list(db: Session, query: ProblemListQuery) -> ProblemListResponse:
    stmt = db.query(Problem).filter(Problem.is_public == True)

    if query.difficulty:
        stmt = stmt.filter(Problem.difficulty == query.difficulty)
    if query.tag:
        stmt = stmt.filter(Problem.tags.contains(query.tag))

    total = stmt.with_entities(func.count()).scalar()

    # 分页
    items = (
        stmt
        .offset((query.page - 1) * query.page_size)
        .limit(query.page_size)
        .all()
    )

    return ProblemListResponse(
        total=total,
        page=query.page,
        page_size=query.page_size,
        items=[ProblemListItem.model_validate(item) for item in items],
    )


def get_problem_detail(db: Session, problem_id: int) -> ProblemDetailResponse:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise ValueError("题目不存在")
    return ProblemDetailResponse.model_validate(problem)


def create_problem(db: Session, data: ProblemCreateRequest) -> ProblemCreateResponse:
    problem = Problem(
        title=data.title,
        difficulty=data.difficulty,
        tags=data.tags,
        description=data.description,
        input_format=data.input_format,
        output_format=data.output_format,
        sample_input=data.sample_input,
        sample_output=data.sample_output,
        hint=data.hint,
        time_limit=data.time_limit,
        memory_limit=data.memory_limit,
        is_public=data.is_public,
    )
    db.add(problem)
    db.commit()
    db.refresh(problem)
    return ProblemCreateResponse.model_validate(problem)


def update_problem(db: Session, problem_id: int, data: ProblemUpdateRequest) -> ProblemCreateResponse:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise ValueError("题目不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(problem, field, value)

    problem.updated_at = datetime.now()
    db.commit()
    db.refresh(problem)
    return ProblemCreateResponse.model_validate(problem)


def delete_problem(db: Session, problem_id: int) -> None:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise ValueError("题目不存在")
    db.delete(problem)
    db.commit()
