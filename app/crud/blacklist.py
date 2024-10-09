from sqlalchemy.orm import Session

from app.model import Blacklist


class CRUDBlacklist:
    def get_by_token(self, db: Session, token: str) -> Blacklist:
        return db.query(Blacklist).filter(Blacklist.token == token).first()

    def create(self, db: Session, *, token: str) -> Blacklist:
        db_obj = Blacklist(token=token)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


blacklist = CRUDBlacklist()
