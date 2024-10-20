from sqlalchemy.orm import Session

from app.model import Account, Manager, Admin
from app.schema.admin import AdminItemResponse
from app.schema.admin import (
    AdminItemResponse,
)


class AdminHelper:
    def get_info_by_account(self, db: Session, account: Account) -> AdminItemResponse:
        manager: Manager = account.manager
        admin: Admin = manager.admin
        return self.get_info(db, account, manager, admin)

    def get_info_by_admin(self, db: Session, admin: Admin) -> AdminItemResponse:
        manager: Manager = admin.manager
        account: Account = manager.account
        return self.get_info(db, account, manager, admin)

    def get_info_by_manager(self, db: Session, manager: Manager) -> AdminItemResponse:
        account: Account = manager.account
        admin: Admin = manager.admin
        return self.get_info(db, account, manager, admin)

    def get_info(
        self, db: Session, account: Account, manager: Manager, admin: Admin
    ) -> AdminItemResponse:
        data_response = {
            **admin.__dict__,
            **{k: v for k, v in manager.__dict__.items() if k != "id"},
            **{k: v for k, v in account.__dict__.items() if k != "id"},
        }
        return AdminItemResponse(**data_response)


admin_helper = AdminHelper()
