from sqlalchemy.orm import Session

from app.model import Manager, Account, Business
from app.schema.business import BusinessItemResponse, BusinessBasicInfoResponse
from app import crud
from app.core.company.company_helper import company_helper
from app.core.location.location_helper import location_helper


class BusinessHelper:
    def get_info_by_account(
        self, db: Session, account: Account
    ) -> BusinessItemResponse:
        manager: Manager = account.manager
        business: Business = manager.business
        return self.get_info(db, account, manager, business)

    def get_info_by_business(
        self, db: Session, business: Business
    ) -> BusinessItemResponse:
        manager: Manager = business.manager
        account: Account = manager.account
        return self.get_info(db, account, manager, business)

    def get_info_by_manager(
        self, db: Session, manager: Manager
    ) -> BusinessItemResponse:
        account: Account = manager.account
        business: Business = manager.business
        return self.get_info(db, account, manager, business)

    def get_info(
        self, db: Session, account: Account, manager: Manager, business: Business
    ) -> BusinessItemResponse:
        data_response = {
            **{
                k: v
                for k, v in business.__dict__.items()
                if k not in ["province", "district", "company"]
            },
            **{k: v for k, v in manager.__dict__.items() if k != "id"},
            **{k: v for k, v in account.__dict__.items() if k != "id"},
        }
        province = location_helper.get_province_info(business.province)
        district = location_helper.get_district_info(business.district)
        company = crud.company.get_by_business_id(db, business.id)
        company_response = company_helper.get_info(db, company)

        return BusinessItemResponse(
            **data_response,
            province=province,
            district=district,
            company=company_response
        )

    def get_basic_info_by_manager(
        self, db: Session, manager: Manager
    ) -> BusinessBasicInfoResponse:
        account: Account = manager.account
        business: Business = manager.business
        return self.get_basic_info(db, account, manager, business)

    def get_basic_info_by_business(
        self, db: Session, business: Business
    ) -> BusinessBasicInfoResponse:
        manager: Manager = business.manager
        account: Account = manager.account
        return self.get_basic_info(db, account, manager, business)

    def get_basic_info_by_account(
        self, db: Session, account: Account
    ) -> BusinessBasicInfoResponse:
        manager: Manager = account.manager
        business: Business = manager.business
        return self.get_basic_info(db, account, manager, business)

    def get_basic_info(
        self, db: Session, account: Account, manager: Manager, business: Business
    ) -> BusinessBasicInfoResponse:
        data_response = {
            **{k: v for k, v in business.__dict__.items() if k not in ["company"]},
            **{k: v for k, v in manager.__dict__.items() if k != "id"},
            **{k: v for k, v in account.__dict__.items() if k != "id"},
        }
        company = crud.company.get_by_business_id(db, business.id)
        company_response = company_helper.get_info_general(company)

        return BusinessBasicInfoResponse(**data_response, company=company_response)


business_helper = BusinessHelper()
