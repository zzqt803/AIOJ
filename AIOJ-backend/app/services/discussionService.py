from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.discussion import Discussion
from app.models.users import User
from app.schemas.discussionSchema import (
    DiscussionListQuery,
    DiscussionListResponse,
    DiscussionItem,
    ReplyItem,
    DiscussionCreateRequest,
    DiscussionCreateResponse,
)


def get_discussion_list(db: Session, problem_id: int, query: DiscussionListQuery) -> DiscussionListResponse:
    # 获取一级评论
    stmt = db.query(Discussion).filter(
        Discussion.problem_id == problem_id,
        Discussion.parent_id.is_(None),
    )

    total = stmt.count()

    discussions = stmt.order_by(Discussion.created_at.desc()).offset(
        (query.page - 1) * query.page_size
    ).limit(query.page_size).all()

    items = []
    for disc in discussions:
        # 获取用户名
        user = db.query(User).filter(User.id == disc.user_id).first()

        # 获取回复
        replies = db.query(Discussion).filter(Discussion.parent_id == disc.id).order_by(Discussion.created_at).all()
        reply_items = []
        for reply in replies:
            reply_user = db.query(User).filter(User.id == reply.user_id).first()
            reply_items.append(ReplyItem(
                id=reply.id,
                user_id=reply.user_id,
                username=reply_user.username if reply_user else "",
                content=reply.content,
                created_at=reply.created_at,
            ))

        items.append(DiscussionItem(
            id=disc.id,
            user_id=disc.user_id,
            username=user.username if user else "",
            content=disc.content,
            replies=reply_items,
            created_at=disc.created_at,
        ))

    return DiscussionListResponse(
        total=total,
        page=query.page,
        page_size=query.page_size,
        items=items,
    )


def create_discussion(db: Session, problem_id: int, data: DiscussionCreateRequest, user_id: int) -> DiscussionCreateResponse:
    # 如果是回复，检查父评论是否存在
    if data.parent_id:
        parent = db.query(Discussion).filter(
            Discussion.id == data.parent_id,
            Discussion.problem_id == problem_id,
        ).first()
        if not parent:
            raise ValueError("父评论不存在")

    discussion = Discussion(
        problem_id=problem_id,
        user_id=user_id,
        content=data.content,
        parent_id=data.parent_id,
    )
    db.add(discussion)
    db.commit()
    db.refresh(discussion)

    user = db.query(User).filter(User.id == user_id).first()

    return DiscussionCreateResponse(
        id=discussion.id,
        problem_id=discussion.problem_id,
        user_id=discussion.user_id,
        username=user.username if user else "",
        content=discussion.content,
        parent_id=discussion.parent_id,
        created_at=discussion.created_at,
    )


def delete_discussion(db: Session, discussion_id: int, user_id: int, is_admin: bool) -> None:
    discussion = db.query(Discussion).filter(Discussion.id == discussion_id).first()
    if not discussion:
        raise ValueError("评论不存在")

    # 只有本人或管理员可以删除
    if discussion.user_id != user_id and not is_admin:
        raise ValueError("无权删除此评论")

    db.delete(discussion)
    db.commit()
