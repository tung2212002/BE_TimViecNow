from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import District
from app.schema.district import (
    DistrictCreate,
    DistrictUpdate,
)


class CRUDDistrict(CRUDBase[District, DistrictCreate, DistrictUpdate]):
    pass


district = CRUDDistrict(District)
