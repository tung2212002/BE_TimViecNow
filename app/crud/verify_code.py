from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import VerifyCode
from app.schema.verify_code import VerifyCodeCreate, VerifyCodeUpdate
from datetime import datetime, timedelta, timezone


class CRUDVerifyCode(CRUDBase[VerifyCode, VerifyCodeCreate, VerifyCodeUpdate]):
    def get_by_code(self, db: Session, code: str) -> VerifyCode:
        return db.query(VerifyCode).filter(VerifyCode.code == code).first()

    def get_by_email(self, db: Session, email: str) -> VerifyCode:
        return db.query(VerifyCode).filter(VerifyCode.email == email).first()

    def get_by_email_and_code(self, db: Session, email, code):
        return (
            db.query(VerifyCode)
            .filter(VerifyCode.email == email, VerifyCode.code == code)
            .first()
        )

    def get_valid_code(self, db: Session, code: str, delta: int) -> VerifyCode:
        return (
            db.query(VerifyCode)
            .filter(VerifyCode.code == code)
            .filter(
                VerifyCode.created_at
                > datetime.now(timezone.utc) - timedelta(minutes=delta)
            )
            .first()
        )

    def get_valid_code_by_session_id_and_email(
        self, db: Session, session_id: str, email: str, delta: int
    ) -> VerifyCode:
        return (
            db.query(VerifyCode)
            .filter(VerifyCode.session_id == session_id, VerifyCode.email == email)
            .filter(
                VerifyCode.created_at
                > datetime.now(timezone.utc) - timedelta(minutes=delta)
            )
            .first()
        )


verify_code = CRUDVerifyCode(VerifyCode)
