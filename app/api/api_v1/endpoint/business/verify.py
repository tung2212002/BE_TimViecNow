from fastapi import (
    APIRouter,
    Depends,
    Body,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.auth.user_manager_service import user_manager_service
from app.core.verify.verify_service import verify_service
from app.hepler.enum import VerifyType

router = APIRouter()


@router.post("/send_verify_code", summary="Send verify code.")
async def send_verify_code(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business),
    data: dict = Body(
        ...,
        example={
            "type": VerifyType.EMAIL,
        },
    ),
    background_tasks: BackgroundTasks = BackgroundTasks(),
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

    return await verify_service.send_verify_background(
        db, background_tasks, data, current_user
    )


@router.post("/verify_code", summary="Verify code.")
async def verify_code(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business),
    data: dict = Body(
        ...,
        example={
            "code": "123456",
            "session_id": "",
        },
    ),
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

    return await verify_service.verify_code(db, data, current_user)
