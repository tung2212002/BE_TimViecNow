from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
import uuid

from app import crud
from app.schema.verify_code import VerifyCodeCreate, VerifyCodeUpdate, VerifyCodeRequest
from app.schema.verify_code_block import VerifyCodeBlockCreate
from app.hepler.enum import VerifyCodeType
from app.core.email.email_service import email_service
from app.core.email.email_hepler import EmailHelper
from app.model import ManagerBase
from app.hepler.common import CommonHelper
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse


class VerifyService:
    async def send_verify_background(
        self,
        db: Session,
        background_tasks: BackgroundTasks,
        data: dict,
        current_user: ManagerBase,
    ):
        if data.get("type") == VerifyCodeType.EMAIL:
            if not current_user.business:
                raise CustomException(
                    status_code=status.HTTP_404_NOT_FOUND, msg="Business not found"
                )

            if current_user.business.is_verified_email:
                raise CustomException(
                    status_code=status.HTTP_400_BAD_REQUEST, msg="Email is verified"
                )

            verify_code_block = crud.verify_code_block.search(
                db, email=current_user.email, delta=5
            )
            if verify_code_block:
                raise CustomException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="Please wait 5 minutes to resend email",
                )

            email_to = current_user.email
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
                manager_base_id=current_user.id,
                email=email_to,
                code=verify_code,
                session_id=session_id,
            )

            crud.verify_code.create(db, obj_in=obj_in)

            response = await email_service.send_email_background(
                db, background_tasks, subject, email_to, body
            )
            if response:
                return CustomResponse(data={"session_id": session_id})

            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Send email failed"
            )

    async def verify_code(self, db: Session, data: dict, current_user: ManagerBase):
        data = VerifyCodeRequest(**data)

        code_block = crud.verify_code_block.search(
            db, email=current_user.email, delta=5
        )
        if code_block:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg="Please wait 5 minutes to resend email",
            )

        code_by_session_id_and_email = (
            crud.verify_code.get_valid_code_by_session_id_and_email(
                db, data.session_id, current_user.email, 5
            )
        )
        if not code_by_session_id_and_email:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Verify code not found"
            )

        if code_by_session_id_and_email.code != data.code:
            if code_by_session_id_and_email.failed_attempts >= 4:
                crud.verify_code.remove(db=db, id=code_by_session_id_and_email.id)
                crud.verify_code_block.create(
                    db,
                    obj_in=VerifyCodeBlockCreate(
                        email=current_user.email,
                        delta=5,
                    ),
                )
                raise CustomException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="Verify code is incorrect. Please wait 5 minutes to resend email",
                )

            crud.verify_code.update(
                db,
                db_obj=code_by_session_id_and_email,
                obj_in=VerifyCodeUpdate(
                    failed_attempts=code_by_session_id_and_email.failed_attempts + 1
                ),
            )
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Verify code is incorrect"
            )

        crud.verify_code.remove(db=db, id=code_by_session_id_and_email.id)
        crud.business.set_is_verified_email(
            db=db, db_obj=current_user.business, is_verified_email=True
        )

        return CustomResponse(msg="Verify code is correct")


verify_service = VerifyService()
