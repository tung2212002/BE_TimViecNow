from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import func

from .base import CRUDBase
from app.model import Conversation, ConversationMember, Message
from app.schema.conversation import ConversationCreate, ConversationUpdate
from app.hepler.enum import ConversationType


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    def get_private_conversation(
        self, db: Session, first_account_id: int, second_account_id: int
    ) -> Conversation:
        return (
            db.query(Conversation)
            .join(
                ConversationMember,
                ConversationMember.conversation_id == Conversation.id,
            )
            .filter(Conversation.type == ConversationType.PRIVATE)
            .filter((ConversationMember.account_id == first_account_id))
            .filter(ConversationMember.account_id == second_account_id)
            .first()
        )

    def get_by_account_id(
        self, db: Session, *, account_id: int, limit: int = 10, skip: int = 0, **kwargs
    ) -> List[Conversation]:
        return (
            db.query(Conversation)
            .join(
                ConversationMember,
                ConversationMember.conversation_id == Conversation.id,
            )
            .filter(ConversationMember.account_id == account_id)
            .limit(limit)
            .offset(skip)
            .all()
        )

    def get_ids_by_account_id(self, db: Session, account_id: int) -> List[int]:
        data = (
            db.query(Conversation.id)
            .join(
                ConversationMember,
                ConversationMember.conversation_id == Conversation.id,
            )
            .filter(ConversationMember.account_id == account_id)
            .all()
        )
        return [d[0] for d in data]

    def get_by_account_id_and_conversation_id(
        self, db: Session, account_id: int, conversation_id: int
    ) -> Conversation:
        return (
            db.query(Conversation)
            .join(
                ConversationMember,
                ConversationMember.conversation_id == Conversation.id,
            )
            .filter(ConversationMember.account_id == account_id)
            .filter(ConversationMember.conversation_id == conversation_id)
            .first()
        )

    def get_by_lastest_message(
        self, db: Session, *, account_id: int, limit: int = 10, skip: int = 0, **kwargs
    ) -> Conversation:
        subquery = (
            db.query(
                Message.conversation_id,
                func.max(Message.created_at).label("latest_message"),
            )
            .group_by(Message.conversation_id)
            .subquery()
        )

        query = (
            db.query(Conversation)
            .join(
                ConversationMember,
                ConversationMember.conversation_id == Conversation.id,
            )
            .join(
                subquery,
                subquery.c.conversation_id == Conversation.id,
            )
            .filter(ConversationMember.account_id == account_id)
            .order_by(subquery.c.latest_message.desc())
            .limit(limit)
            .offset(skip)
        )

        return query.all()


conversation = CRUDConversation(Conversation)
