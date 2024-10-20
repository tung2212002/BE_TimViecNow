from sqlalchemy.orm import Session

from app.model import User, Account
from app.schema.user import UserItemResponse, UserBasicResponse


class UserHelper:
    def get_info_by_account(self, db: Session, account: Account) -> UserItemResponse:
        user: User = account.user
        return self.get_info(db, account, user)

    def get_info_by_user(self, db: Session, user: User) -> UserItemResponse:
        account: Account = user.account
        return self.get_info(db, account, user)

    def get_info(self, db: Session, account: Account, user: User) -> UserItemResponse:
        data_response = {
            **user.__dict__,
            **{k: v for k, v in account.__dict__.items() if k != "id"},
        }

        return UserItemResponse(
            **data_response,
        )

    def get_basic_info(
        self, db: Session, account: Account, user: User
    ) -> UserBasicResponse:
        data_response = {
            **user.__dict__,
            **{k: v for k, v in account.__dict__.items() if k != "id"},
        }

        return UserBasicResponse(
            **data_response,
        )

    def get_basic_info_by_account(
        self, db: Session, account: Account
    ) -> UserBasicResponse:
        user: User = account.user
        return self.get_basic_info(db, account, user)

    def get_basic_info_by_user(self, db: Session, user: User) -> UserBasicResponse:
        account: Account = user.account
        return self.get_basic_info(db, account, user)


user_helper = UserHelper()
