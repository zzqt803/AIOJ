from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.problem_set import ProblemSet, ProblemSetItem
from app.models.problems import Problem
from app.models.users import User
from app.schemas.problemSetSchema import (
    ProblemSetListQuery,
    ProblemSetListResponse,
    ProblemSetListItem,
    ProblemSetDetailResponse,
    ProblemInSet,
    ProblemSetCreateRequest,
    ProblemSetCreateResponse,
    ProblemSetUpdateRequest,
    ProblemSetItemAddRequest,
    ProblemSetItemAddResponse,
)
from datetime import datetime


def get_problem_set_list(db: Session, query: ProblemSetListQuery) -> ProblemSetListResponse:
    # 使用视图查询
    stmt = db.query(
        ProblemSet.id,
        ProblemSet.title,
        ProblemSet.description,
        ProblemSet.is_public,
        ProblemSet.created_at,
        User.username.label("creator_name"),
        func.count(ProblemSetItem.id).label("problem_count"),
    ).join(
        User, User.id == ProblemSet.creator_id
    ).outerjoin(
        ProblemSetItem, ProblemSetItem.problem_set_id == ProblemSet.id
    ).filter(
        ProblemSet.is_public == True
    ).group_by(
        ProblemSet.id, ProblemSet.title, ProblemSet.description,
        ProblemSet.is_public, ProblemSet.created_at, User.username
    )

    total = db.query(func.count(ProblemSet.id)).filter(ProblemSet.is_public == True).scalar()

    items = stmt.order_by(ProblemSet.created_at.desc()).offset(
        (query.page - 1) * query.page_size
    ).limit(query.page_size).all()

    return ProblemSetListResponse(
        total=total,
        page=query.page,
        page_size=query.page_size,
        items=[ProblemSetListItem.model_validate(item) for item in items],
    )


def get_problem_set_detail(db: Session, problem_set_id: int) -> ProblemSetDetailResponse:
    problem_set = db.query(ProblemSet).filter(ProblemSet.id == problem_set_id).first()
    if not problem_set:
        raise ValueError("题单不存在")

    # 获取创建者名称
    creator = db.query(User).filter(User.id == problem_set.creator_id).first()

    # 获取题单中的题目
    problems = (
        db.query(
            ProblemSetItem.problem_id,
            ProblemSetItem.sort_order,
            Problem.title,
            Problem.difficulty,
        )
        .join(Problem, Problem.id == ProblemSetItem.problem_id)
        .filter(ProblemSetItem.problem_set_id == problem_set_id)
        .order_by(ProblemSetItem.sort_order)
        .all()
    )

    return ProblemSetDetailResponse(
        id=problem_set.id,
        title=problem_set.title,
        description=problem_set.description,
        creator_id=problem_set.creator_id,
        creator_name=creator.username if creator else "",
        is_public=problem_set.is_public,
        problems=[ProblemInSet.model_validate({
            "problem_id": p.problem_id,
            "sort_order": p.sort_order,
            "title": p.title,
            "difficulty": p.difficulty.value if hasattr(p.difficulty, 'value') else p.difficulty,
        }) for p in problems],
        created_at=problem_set.created_at,
    )


def create_problem_set(db: Session, data: ProblemSetCreateRequest, creator_id: int) -> ProblemSetCreateResponse:
    problem_set = ProblemSet(
        title=data.title,
        description=data.description,
        creator_id=creator_id,
        is_public=data.is_public,
    )
    db.add(problem_set)
    db.commit()
    db.refresh(problem_set)
    return ProblemSetCreateResponse.model_validate(problem_set)


def update_problem_set(db: Session, problem_set_id: int, data: ProblemSetUpdateRequest) -> ProblemSetCreateResponse:
    problem_set = db.query(ProblemSet).filter(ProblemSet.id == problem_set_id).first()
    if not problem_set:
        raise ValueError("题单不存在")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(problem_set, field, value)

    problem_set.updated_at = datetime.now()
    db.commit()
    db.refresh(problem_set)
    return ProblemSetCreateResponse.model_validate(problem_set)


def delete_problem_set(db: Session, problem_set_id: int) -> None:
    problem_set = db.query(ProblemSet).filter(ProblemSet.id == problem_set_id).first()
    if not problem_set:
        raise ValueError("题单不存在")
    db.delete(problem_set)
    db.commit()


def add_problem_to_set(db: Session, problem_set_id: int, data: ProblemSetItemAddRequest) -> ProblemSetItemAddResponse:
    # 检查题单是否存在
    problem_set = db.query(ProblemSet).filter(ProblemSet.id == problem_set_id).first()
    if not problem_set:
        raise ValueError("题单不存在")

    # 检查题目是否存在
    problem = db.query(Problem).filter(Problem.id == data.problem_id).first()
    if not problem:
        raise ValueError("题目不存在")

    # 检查是否已存在
    existing = db.query(ProblemSetItem).filter(
        ProblemSetItem.problem_set_id == problem_set_id,
        ProblemSetItem.problem_id == data.problem_id,
    ).first()
    if existing:
        raise ValueError("题目已在题单中")

    item = ProblemSetItem(
        problem_set_id=problem_set_id,
        problem_id=data.problem_id,
        sort_order=data.sort_order,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return ProblemSetItemAddResponse.model_validate(item)


def remove_problem_from_set(db: Session, problem_set_id: int, problem_id: int) -> None:
    item = db.query(ProblemSetItem).filter(
        ProblemSetItem.problem_set_id == problem_set_id,
        ProblemSetItem.problem_id == problem_id,
    ).first()
    if not item:
        raise ValueError("题目不在题单中")
    db.delete(item)
    db.commit()
