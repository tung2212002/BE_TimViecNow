from fastapi import status
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app.crud import (
    verify_code as verify_codeCRUD,
    verify_code_block as verify_code_blockCRUD,
    business as businessCRUD,
)
from app.schema.verify_code import VerifyCodeCreate, VerifyCodeUpdate, VerifyCodeRequest
from app.schema.verify_code_block import VerifyCodeBlockCreate
from app.hepler.enum import VerifyCodeType
from app.core.email.email_service import email_service
from app.core.email.email_hepler import EmailHelper
from app.model import Manager, Account, Business
from app.hepler.common import CommonHelper
from app.common.exception import CustomException
from app.common.response import CustomResponse


class VerifyService:
    async def send_verify_background(
        self,
        db: Session,
        background_tasks: BackgroundTasks,
        data: dict,
        current_user: Account,
    ):
        if data.get("type") == VerifyCodeType.EMAIL:
            manager: Manager = current_user.manager
            business: Business = manager.business
            if business.is_verified_email:
                raise CustomException(
                    status_code=status.HTTP_400_BAD_REQUEST, msg="Email is verified"
                )

            verify_code_block = verify_code_blockCRUD.search(
                db, email=manager.email, delta=5
            )
            if verify_code_block:
                raise CustomException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="Please wait 5 minutes to resend email",
                )

            email_to = manager.email
            subject = "Verify Email"
            verify_code = CommonHelper.generate_code(6)
            session_id = str(uuid.uuid4())

            body = EmailHelper.fill_template(
                EmailHelper.read_email_templates("email.html"),
                email=email_to,
                verify_code=verify_code,
                full_name=current_user.full_name,
                title="xác thực tài khoản",
            )

            obj_in = VerifyCodeCreate(
                manager_id=current_user.id,
                email=email_to,
                code=verify_code,
                session_id=session_id,
            )

            verify_codeCRUD.create(db, obj_in=obj_in)

            response = await email_service.send_email_background(
                db, background_tasks, subject, email_to, body
            )
            if response:
                return CustomResponse(data={"session_id": session_id})

            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Send email failed"
            )

    async def verify_code(self, db: Session, data: dict, current_user: Account):
        code_data = VerifyCodeRequest(**data)

        manager: Manager = current_user.manager
        code_block = verify_code_blockCRUD.search(db, email=manager.email, delta=5)
        if code_block:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg="Please wait 5 minutes to resend email",
            )

        code_by_session_id_and_email = (
            verify_codeCRUD.get_valid_code_by_session_id_and_email(
                db, code_data.session_id, manager.email, 5
            )
        )
        if not code_by_session_id_and_email:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Verify code not found"
            )

        if code_by_session_id_and_email.code != code_data.code:
            if code_by_session_id_and_email.failed_attempts >= 4:
                verify_codeCRUD.remove(db=db, id=code_by_session_id_and_email.id)
                verify_code_blockCRUD.create(
                    db,
                    obj_in=VerifyCodeBlockCreate(
                        email=manager.email,
                        delta=5,
                    ),
                )
                raise CustomException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="Verify code is incorrect. Please wait 5 minutes to resend email",
                )

            verify_codeCRUD.update(
                db,
                db_obj=code_by_session_id_and_email,
                obj_in=VerifyCodeUpdate(
                    failed_attempts=code_by_session_id_and_email.failed_attempts + 1
                ),
            )
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Verify code is incorrect"
            )

        verify_codeCRUD.remove(db=db, id=code_by_session_id_and_email.id)
        businessCRUD.set_is_verified_email(
            db=db, db_obj=manager.business, is_verified_email=True
        )

        return CustomResponse(msg="Verify code is correct")


verify_service = VerifyService()
