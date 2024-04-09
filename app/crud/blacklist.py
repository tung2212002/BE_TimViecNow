from sqlalchemy.orm import Session

from app.model.blacklist import Blacklist


class CRUDBlacklist:
    def get_by_token(self, db: Session, token: str) -> Blacklist:
        return db.query(Blacklist).filter(Blacklist.token == token).first()

    def create(self, db: Session, *, token: str) -> Blacklist:
        print("token", token)
        print("size of token", len(token))
        db_obj = Blacklist(token=token)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


blacklist = CRUDBlacklist()
