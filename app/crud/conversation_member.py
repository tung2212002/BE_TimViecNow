from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import case
from typing import List

from .base import CRUDBase
from app.model import ConversationMember, Account, Message
from app.schema.conversation_member import (
    ConversationMemberCreate,
    ConversationMemberUpdate,
)
from app.hepler.enum import MemberType


class CRUDConversationMember(
    CRUDBase[ConversationMember, ConversationMemberCreate, ConversationMemberUpdate]
):
    def get_by_account_ids(self, db: Session, account_ids: list[int]) -> int:
        num_users = len(account_ids)
        return (
            db.query(ConversationMember.conversation_id)
            .filter(ConversationMember.account_id.in_(account_ids))
            .group_by(ConversationMember.conversation_id)
            .having(func.count(ConversationMember.account_id) == num_users)
            .having(
                func.count(func.distinct(ConversationMember.account_id)) == num_users
            )
            .limit(1)
            .scalar()
        )

    # SELECT group_id
    # FROM group_users
    # WHERE user_id IN (user_id1, user_id2, user_id3, ...)
    # GROUP BY group_id
    # HAVING COUNT(user_id) = X -- X là số lượng người dùng trong nhóm
    # AND COUNT(DISTINCT user_id) = X; -- Đảm bảo rằng không có user nào bị trùng
    # LIMIT 1;

    def get_member_by_conversation_id(
        self,
        db: Session,
        *,
        conversation_id: int,
        limit: int = 10,
        skip: int = 0
        # ) -> ConversationMember:
        #     role_priority = case(
        #         [
        #             (ConversationMember.type == MemberType.ADMIN, 1),
        #             (ConversationMember.type == MemberType.MEMBER, 2),
        #         ],
        #         else_=3,
        #     )
        #     return (
        #         db.query(ConversationMember)
        #         .filter_by(conversation_id=conversation_id)
        #         .order_by(role_priority)
        #         .limit(limit)
        #         .offset(skip)
        #         .all()
        #     )
    ) -> List[Account]:
        role_priority = case(
            (ConversationMember.type == MemberType.ADMIN, 1),
            (ConversationMember.type == MemberType.MEMBER, 2),
            else_=3,
        )
        return (
            db.query(Account)
            .join(
                ConversationMember,
                ConversationMember.account_id == Account.id,
            )
            .filter(ConversationMember.conversation_id == conversation_id)
            .order_by(role_priority)
            .limit(limit)
            .offset(skip)
            .all()
        )

    def get_by_conversation_id(
        self, db: Session, *, conversation_id: int, limit: int = 10, skip: int = 0
    ) -> ConversationMember:
        role_priority = case(
            (ConversationMember.type == MemberType.ADMIN, 1),
            (ConversationMember.type == MemberType.MEMBER, 2),
            else_=3,
        )
        return (
            db.query(ConversationMember)
            .filter_by(conversation_id=conversation_id)
            .order_by(role_priority)
            .limit(limit)
            .offset(skip)
            .all()
        )

    def get_by_account_id_and_conversation_id(
        self, db: Session, *, account_id: int, conversation_id: int
    ) -> ConversationMember:
        return (
            db.query(ConversationMember)
            .filter_by(account_id=account_id, conversation_id=conversation_id)
            .first()
        )


conversation_member = CRUDConversationMember(ConversationMember)
