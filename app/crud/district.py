from sqlalchemy.orm import Session
from typing import List

from .base import CRUDBase
from app.model import District
from app.schema.district import (
    DistrictCreate,
    DistrictUpdate,
)


class CRUDDistrict(CRUDBase[District, DistrictCreate, DistrictUpdate]):
    def get_multi_by_province(
        self,
        db: Session,
        *,
        province_id: int,
        skip: int = 0,
        limit: int = 1000,
        sort_by: str = "id",
        order_by: str = "asc",
    ) -> List[District]:
        return (
            db.query(self.model)
            .filter(self.model.province_id == province_id)
            .order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "asc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


district = CRUDDistrict(District)
