from sqlalchemy.orm import Session

from app.model import PinnedMessage
from app.schema.pinned_message import PinnedMessageCreate


class CRUDPinnedMessage:
    def get(self, db: Session, id: int) -> PinnedMessage:
        return db.query(PinnedMessage).filter(PinnedMessage.id == id).first()

    def create(self, db: Session, obj_in: PinnedMessageCreate) -> PinnedMessage:
        db_obj = PinnedMessage(
            message_id=obj_in.message_id,
            conversation_id=obj_in.conversation_id,
            account_id=obj_in.account_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, id: int) -> None:
        db.query(PinnedMessage).filter(PinnedMessage.id == id).delete()
        db.commit()


pinned_message = CRUDPinnedMessage()
