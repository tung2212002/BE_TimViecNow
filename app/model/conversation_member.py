from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Index, DateTime, event
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.hepler.enum import MemberType


class ConversationMember(Base):
    account_id = Column(
        Integer,
        ForeignKey("account.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    conversation_id = Column(
        Integer,
        ForeignKey("conversation.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    last_read_message_id = Column(Integer, nullable=True)
    last_read_at = Column(DateTime(timezone=True), nullable=True)
    type = Column(Enum(MemberType), default=MemberType.MEMBER, nullable=False)
    nickname = Column(String(50), nullable=True)

    account = relationship("Account", back_populates="conversation_member_secondary")
    conversation = relationship(
        "Conversation", back_populates="conversation_member_secondary"
    )

    __table_args__ = (
        Index("idx_account_id_conversation_id", account_id, conversation_id),
        Index(
            "idx_account_id_conversation_id_last_read_message_id",
            account_id,
            conversation_id,
            last_read_message_id,
        ),
    )
