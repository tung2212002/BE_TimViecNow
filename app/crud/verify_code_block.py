from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone


from app.model import VerifyCodeBlock
from app.schema.verify_code_block import VerifyCodeBlockCreate


class CRUDVerifyCodeBlock:

    def create(self, db: Session, *, obj_in: VerifyCodeBlockCreate) -> VerifyCodeBlock:
        db_obj = VerifyCodeBlock(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, db: Session, email: str) -> VerifyCodeBlock:
        return db.query(VerifyCodeBlock).filter(VerifyCodeBlock.email == email).first()

    def search(self, db: Session, *, email: str, delta: int) -> VerifyCodeBlock:
        return (
            db.query(VerifyCodeBlock)
            .filter(VerifyCodeBlock.email == email)
            .filter(
                VerifyCodeBlock.created_at
                > datetime.now(timezone.utc) - timedelta(minutes=delta)
            )
            .first()
        )


verify_code_block = CRUDVerifyCodeBlock()
