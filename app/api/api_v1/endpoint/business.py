from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    File,
    UploadFile,
    Form,
    Body,
    Query,
    Path,
)
from sqlalchemy.orm import Session
from typing import Annotated, Any

from app.db.base import get_db
from app.core.auth.service_business_auth import (
    get_current_user,
    get_current_admin,
)
from app.core import constant
from app.core.business import service_business
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("/me", summary="Get the current business.")
def get_business(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get the current business.

    This endpoint allows getting the current business.

    Returns:
    - status_code (200): The current user has been found successfully.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_business.get_me(db, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("", summary="Get list of business.")
def get_business(
    request: Request,
    skip: int = Query(description="The number of users to skip.", example=0),
    limit: int = Query(description="The number of users to return.", example=10),
    sort_by: str = Query(description="The field to sort by.", example="id"),
    order_by: str = Query(description="The order to sort by.", example="desc"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Get list of business by admin.

    This endpoint allows getting a list of business by admin.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of users has been found successfully.
    - status_code (404): The list of users is not found.
    - status_code (401): The user is not authorized.
    - status_code (400): The request is invalid.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_business.get_list_business(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get a business by id.")
def get_user_bbusiness(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Get a business by id.

    This endpoint allows getting a business by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been found successfully.
    - status_code (404): The user is not found.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_business.get_business_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Register a new business by admin.")
def create_business(
    full_name: Annotated[str, Form(..., description="The full name of the business.")],
    email: Annotated[str, Form(..., description="The email of the business.")],
    password: Annotated[str, Form(..., description="The password of the business.")],
    confirm_password: Annotated[
        str, Form(..., description="The confirm password of the business.")
    ],
    province_id: Annotated[
        int, Form(..., description="The province id of the business.")
    ],
    phone_number: Annotated[
        str, Form(..., description="The phone number of the business.")
    ],
    gender: Annotated[str, Form(..., description="Gender of the business.")],
    company_name: Annotated[
        str, Form(..., description="The name company of the business.")
    ],
    work_position: Annotated[
        str, Form(..., description="The work position of the business.")
    ],
    work_location: str = Form(None, description="The work location of the business."),
    avatar: UploadFile = File(None, description="The profile avatar of the business."),
    district_id: int = Form(None, description="The district id of the business."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Register a new business by admin.

    This endpoint allows create a new business by admin.

    Parameters:
    - full_name (str): The full name of the business.
    - email (str): The email of the business.
    - password (str): The password of the business.
    - confirm_password (str): The confirm password of the business.
    - avatar (UploadFile): The profile avatar of the business.
    - province_id (int): The province id of the business.
    - district_id (int): The district id of the business.
    - phone_number (str): The phone number of the business.
    - gender (str): The gender of the business.
    - company (str): The company of the business.
    - work_position (str): The work position of the business.
    - work_location (str): The work location of the business.

    Returns:
    - status_code (201): The business has been registered successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The business is already registered.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_business.create_business(db, data)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a business.")
def update_business(
    id: int = Path(..., description="The id of the user.", example=1),
    full_name: str = Form(None, description="The full name of the user."),
    phone_number: str = Form(None, description="The phone number of the user."),
    avatar: UploadFile = File(None, description="The profile avatar of the user."),
    province_id: int = Form(None, description="The province id of the user."),
    district_id: int = Form(None, description="The district id of the user."),
    work_position: str = Form(None, description="The work position of the user."),
    work_location: str = Form(None, description="The work location of the user."),
    company: str = Form(None, description="The company of the user."),
    gender: str = Form(None, description="Gender of the user."),
    password: str = Form(None, description="The password of the user."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update a business.

    This endpoint allows updating a business with the provided information,

    Parameters:
    - id (int): The id of the user.
    - full_name (str): The full name of the user.
    - email (str): The email address of the user.
    - phone_number (str): The phone number of the user.
    - avatar (UploadFile): The profile avatar of the user.
    - province_id (int): The province id of the user.
    - district_id (int): The district id of the user.
    - work_position (str): The work position of the user.
    - work_location (str): The work location of the user.
    - company (str): The company of
    - gender (str): The gender of the user.
    - password (str): The password of the user.

    Returns:
    - status_code (200): The user has been updated successfully.
    - status_code (401): User is not authorized.
    - status_code (400): The request is invalid.
    - status_code (404): The user is not found.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_business.update_business(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a business.")
def delete_business(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a business.

    This endpoint allows deleting a business by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been deleted successfully.
    - status_code (401): User is not authorized.
    - status_code (404): The user is not found.

    """

    status, status_code, response = service_business.delete_business(
        db, id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
