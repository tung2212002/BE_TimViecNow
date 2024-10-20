from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import MessageReaction

from app.schema.message_reaction import (
    MessageReactionCreate,
)


class CRUDMessageReaction:
    def get(self, db: Session, id: int) -> MessageReaction:
        return db.query(MessageReaction).filter(MessageReaction.id == id).first()

    def get_by_account_id_and_message_id(
        self, db: Session, account_id: int, message_id: int
    ) -> MessageReaction:
        return (
            db.query(MessageReaction)
            .filter(
                MessageReaction.account_id == account_id,
                MessageReaction.message_id == message_id,
            )
            .first()
        )

    def create(self, db: Session, obj_in: MessageReactionCreate) -> MessageReaction:
        db_obj = MessageReaction(
            message_id=obj_in.message_id, account_id=obj_in.account_id, type=obj_in.type
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> None:
        db.query(MessageReaction).filter(MessageReaction.id == id).delete()
        db.commit()


message_reaction = CRUDMessageReaction()
