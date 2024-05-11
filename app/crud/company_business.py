from .base import CRUDBase
from app.model.company_business import CompanyBusiness
from app.schema.company_business import CompanyBusinessCreate, CompanyBusinessUpdate


class CRUDCompanyBusiness(
    CRUDBase[CompanyBusiness, CompanyBusinessCreate, CompanyBusinessUpdate]
):
    pass


company_business = CRUDCompanyBusiness(CompanyBusiness)
