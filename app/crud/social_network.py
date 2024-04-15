from typing import List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from .base import CRUDBase
from app.model.social_network import SocialNetwork
from app.schema import social_network as schema_social_network
from app.hepler.enum import Role


class CRUDSocialNetwork(
    CRUDBase[
        SocialNetwork,
        schema_social_network.SocialNetworkCreateRequest,
        schema_social_network.SocialNetworkUpdateRequest,
    ]
):

    def get_by_email(self, db: Session, email: str) -> SocialNetwork:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "id",
        order_by: str = "desc"
    ) -> List[SocialNetwork]:
        return super().get_multi(
            db, skip=skip, limit=limit, sort_by=sort_by, order_by=order_by
        )

    def create(
        self, db: Session, *, obj_in: schema_social_network.SocialNetworkCreateRequest
    ) -> SocialNetwork:
        db_obj = SocialNetwork(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def is_active(self, social_network: SocialNetwork) -> bool:
        return social_network.is_active

    def is_supersocial_network(self, social_network: SocialNetwork) -> bool:
        return social_network.role == Role.SUPER_USER

    def set_active(
        self, db: Session, *, db_obj: SocialNetwork, is_active: bool
    ) -> SocialNetwork:
        db_obj.is_active = is_active
        db.commit()
        db.refresh(db_obj)
        return db_obj


social_network = CRUDSocialNetwork(SocialNetwork)
