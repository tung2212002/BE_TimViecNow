from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import aliased

from .base import CRUDBase
from app.model import Message, ConversationMember
from app.schema.message import MessageCreate, MessageUpdate


class MessageCRUD(CRUDBase[Message, MessageCreate, MessageUpdate]):
    def get_by_conversation_id(
        self,
        db: Session,
        *,
        conversation_id: int,
        limit: int = 20,
        skip: int = 0,
        **kwargs
    ):
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
            .offset(skip)
            .all()
        )

    def get_count_message_unread_by_account_id_and_conversation_id(
        self, db: Session, account_id: int, conversation_id: int
    ) -> int:
        return (
            db.query(func.count(Message.id))
            .join(
                ConversationMember,
                ConversationMember.conversation_id == Message.conversation_id,
            )
            .filter(
                Message.conversation_id == conversation_id,
                Message.created_at > ConversationMember.last_read_at,
                ConversationMember.account_id == account_id,
            )
            .scalar()
        )


message = MessageCRUD(Message)
