from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import Province
from app.schema.province import (
    ProvinceCreate,
    ProvinceUpdate,
)


class CRUDProvince(CRUDBase[Province, ProvinceCreate, ProvinceUpdate]):
    pass


province = CRUDProvince(Province)
