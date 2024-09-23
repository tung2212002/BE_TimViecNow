from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    Form,
    Query,
    Path,
)
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core.auth.user_manager_service import user_manager_service
from app.core.business.business_service import business_service
from app.hepler.enum import OrderType, SortBy, Gender

router = APIRouter()


@router.get("/me", summary="Get the current business.")
async def get_business(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
):
    """
    Get the current business.

    This endpoint allows getting the current business.

    Returns:
    - status_code (200): The current user has been found successfully.
    - status_code (401): The user is not authorized.

    """
    return await business_service.get_me(db, current_user)


@router.get("", summary="Get list of business.")
async def get_business(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=10),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.ASC
    ),
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
    args = locals()

    return await business_service.get(db, args)


@router.get("/{id}", summary="Get a business by id.")
async def get_user_bbusiness(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    id: int = Path(..., description="The id of the user.", example=1),
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
    return await business_service.get_by_id(db, id)


@router.post("", summary="Register a new business by admin.")
async def create_business(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_admin),
    full_name: str = Form(
        ...,
        description="The full name of the business.",
        json_schema_extra={"example": "Tung Ong"},
    ),
    email: str = Form(
        ...,
        description="The email of the business.",
        json_schema_extra={"example": "tungong@email.com"},
    ),
    password: str = Form(
        ...,
        description="The password of the business.",
        json_schema_extra={"example": "@Password1234"},
    ),
    confirm_password: str = Form(
        ...,
        description="The confirm password of the business.",
        json_schema_extra={"example": "@Password1234"},
    ),
    province_id: int = Form(
        ...,
        description="The province id of the business.",
        json_schema_extra={"example": 1},
    ),
    phone_number: str = Form(
        ...,
        description="The phone number of the business.",
        json_schema_extra={"example": "0323456789"},
    ),
    gender: Gender = Form(
        ...,
        description="Gender of the business.",
        json_schema_extra={"example": Gender.OTHER},
    ),
    company_name: str = Form(
        ...,
        description="The company of the business.",
        json_schema_extra={"example": "Tung Ong Company"},
    ),
    work_position: str = Form(
        ...,
        description="The work position of the business.",
        json_schema_extra={"example": "Nhân viên"},
    ),
    work_location: str = Form(
        None,
        description="The work location of the business.",
        json_schema_extra={"example": "Hà Nội"},
    ),
    avatar: UploadFile = File(None, description="The profile avatar of the business."),
    district_id: int = Form(
        None,
        description="The district id of the business.",
        json_schema_extra={"example": 1},
    ),
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
    data = locals()

    return await business_service.create(db, data)


@router.put("/{id}", summary="Update a business.")
async def update_business(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business),
    id: int = Path(..., description="The id of the user.", example=1),
    full_name: str = Form(
        None,
        description="The full name of the business.",
        json_schema_extra={"example": "Tung Ong"},
    ),
    province_id: int = Form(
        None,
        description="The province id of the business.",
        json_schema_extra={"example": 1},
    ),
    phone_number: str = Form(
        None,
        description="The phone number of the business.",
        json_schema_extra={"example": "0323456789"},
    ),
    gender: Gender = Form(
        None,
        description="Gender of the business.",
        json_schema_extra={"example": Gender.OTHER},
    ),
    company_name: str = Form(
        None,
        description="The company of the business.",
        json_schema_extra={"example": "Tung Ong Company"},
    ),
    work_position: str = Form(
        None,
        description="The work position of the business.",
        json_schema_extra={"example": "Nhân viên"},
    ),
    work_location: str = Form(
        None,
        description="The work location of the business.",
        json_schema_extra={"example": "Hà Nội"},
    ),
    avatar: UploadFile = File(None, description="The profile avatar of the business."),
    district_id: int = Form(
        None,
        description="The district id of the business.",
        json_schema_extra={"example": 1},
    ),
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
    - company_name (str): The company of the user.
    - gender (str): The gender of the user.

    Returns:
    - status_code (200): The user has been updated successfully.
    - status_code (401): User is not authorized.
    - status_code (400): The request is invalid.
    - status_code (404): The user is not found.

    """
    data = locals()

    return await business_service.update(db, data, current_user)


@router.delete("/{id}", summary="Delete a business.")
async def delete_business(
    db: Session = Depends(get_db),
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
    id: int = Path(..., description="The id of the user.", example=1),
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
    return await business_service.delete(db, id, current_user)
