from fastapi import (
    APIRouter,
    Depends,
    Body,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core import constant
from app.core.verify import service_verify
from app.core.auth.service_business_auth import get_current_user
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import VerifyType

router = APIRouter()


@router.post("/send_verify_code", summary="Send verify code.")
async def send_verify_code(
    data: dict = Body(
        ...,
        example={
            "type": VerifyType.EMAIL,
        },
    ),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Send verify code.

    This endpoint allows sending verify code.

    Parameters:
    - type (str): The type of verify.

    Returns:
    - status_code (200): The verify code has been sent successfully.
    - status_code (400): The request is invalid.
    - status_code (401): The business is not authorized.
    - status_code (404): The business is not found.

    """

    status, status_code, response = await service_verify.send_verify_background(
        db, background_tasks, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("/verify_code", summary="Verify code.")
def verify_code(
    data: dict = Body(
        ...,
        example={
            "code": "123456",
            "session_id": "",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Verify code.

    This endpoint allows verifying code.

    Parameters:
    - type (str): The type of verify.
    - code (str): The code to verify.

    Returns:
    - status_code (200): The code has been verified successfully.
    - status_code (400): The request is denied.
    - status_code (401): The business is not authorized.
    - status_code (404): The business is not found or the code is incorrect.

    """

    status, status_code, response = service_verify.verify_code(db, data, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
