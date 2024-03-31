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
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.base import get_db
from app.core.auth.service_business_auth import (
    get_current_user,
    get_current_superuser,
    get_current_admin,
)
from app.core import constant
from app.core.representative import service_representative
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("/me", summary="Get the current representative.")
def gerepresentative(current_user=Depends(get_current_user)):
    """
    Get the current representative.

    This endpoint allows getting the current representative.

    Returns:
    - status_code (200): The current user has been found successfully.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_representative.get_me(current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("", summary="Get list of representative.")
def get_representative(
    request: Request,
    skip: int = Query(description="The number of users to skip.", example=0),
    limit: int = Query(description="The number of users to return.", example=10),
    sort_by: str = Query(description="The field to sort by.", example="id"),
    order_by: str = Query(description="The order to sort by.", example="asc"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Get list of representative by admin.

    This endpoint allows getting a list of representative by admin.

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

    status, status_code, response = service_representative.get_list_representative(
        db, args
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get a representative by id.")
def get_user_brepresentative(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Get a representative by id.

    This endpoint allows getting a representative by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been found successfully.
    - status_code (404): The user is not found.
    - status_code (401): The user is not authorized.

    """
    status, status_code, response = service_representative.get_representative_by_id(
        db, id
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Register a new representative by admin.")
def create_representative(
    full_name: Annotated[
        str, Form(..., description="The full name of the representative.")
    ],
    email: Annotated[str, Form(..., description="The email of the representative.")],
    password: Annotated[
        str, Form(..., description="The password of the representative.")
    ],
    confirm_password: Annotated[
        str, Form(..., description="The confirm password of the representative.")
    ],
    province_id: Annotated[
        int, Form(..., description="The province id of the representative.")
    ],
    phone_number: Annotated[
        str, Form(..., description="The phone number of the representative.")
    ],
    gender: Annotated[str, Form(..., description="Gender of the representative.")],
    company: Annotated[
        str, Form(..., description="The company of the representative.")
    ],
    work_position: Annotated[
        str, Form(..., description="The work position of the representative.")
    ],
    work_location: str = Form(
        None, description="The work location of the representative."
    ),
    avatar: UploadFile = File(
        None, description="The profile avatar of the representative."
    ),
    district_id: int = Form(None, description="The district id of the representative."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin),
):
    """
    Register a new representative by admin.

    This endpoint allows create a new representative by admin.

    Parameters:
    - full_name (str): The full name of the representative.
    - email (str): The email of the representative.
    - password (str): The password of the representative.
    - confirm_password (str): The confirm password of the representative.
    - avatar (UploadFile): The profile avatar of the representative.
    - province_id (int): The province id of the representative.
    - district_id (int): The district id of the representative.
    - phone_number (str): The phone number of the representative.
    - gender (str): The gender of the representative.
    - company (str): The company of the representative.
    - work_position (str): The work position of the representative.
    - work_location (str): The work location of the representative.

    Returns:
    - status_code (201): The representative has been registered successfully.
    - status_code (400): The request is invalid.
    - status_code (409): The representative is already registered.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}
    status, status_code, response = service_representative.create_representative(
        db, data
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a representative.")
def update_representative(
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
    Update a representative.

    This endpoint allows updating a representative with the provided information,

    Parameters:
    - id (int): The id of the user.
    - full_name (str): The full name of the user.
    - email (str): The email address of the user.
    - phone_number (str): The phone number of the user.
    - avatar (UploadFile): The profile avatar of the user.

    Returns:
    - status_code (200): The user has been updated successfully.
    - status_code (401): User is not authorized.
    - status_code (400): The request is invalid.
    - status_code (404): The user is not found.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_representative.update_representative(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a representative.")
def delete_representative(
    id: int = Path(..., description="The id of the user.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a representative.

    This endpoint allows deleting a representative by id.

    Parameters:
    - id (int): The id of the user.

    Returns:
    - status_code (200): The user has been deleted successfully.
    - status_code (401): User is not authorized.
    - status_code (404): The user is not found.

    """

    status, status_code, response = service_representative.delete_representative(
        db, id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
