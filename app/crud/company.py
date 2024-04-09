from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import Company
from app.schema.company import CompanyCreateRequest, CompanyUpdateRequest


class CRUDCompany(CRUDBase[Company, CompanyCreateRequest, CompanyUpdateRequest]):
    pass


company = CRUDCompany(Company)
