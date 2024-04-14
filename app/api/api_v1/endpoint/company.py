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
from typing import Annotated, Any, List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.db.base import get_db
from app.core.auth.service_business_auth import get_current_user
from app.core import constant
from app.core.company import service_company
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("", summary="Get list of companies.")
def get_companies(
    request: Request,
    skip: int = Query(0, description="The number of companies to skip.", example=0),
    limit: int = Query(
        10, description="The number of companies to return.", example=10
    ),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
    db: Session = Depends(get_db),
):
    """
    Get list of companies.

    This endpoint allows getting a list of companies.

    Parameters:
    - skip (int): The number of companies to skip.
    - limit (int): The number of companies to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.

    Returns:
    - status_code (200): The list of companies has been found successfully.
    - status_code (404): The list of companies is not found.
    - status_code (400): The request is invalid.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status, status_code, response = service_company.get_list_company(db, args)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get a company by id.")
def get_company_by_id(
    id: int = Path(..., description="The id of the company.", example=1),
    db: Session = Depends(get_db),
):
    """
    Get a company by id.

    This endpoint allows getting a company by id.

    Parameters:
    - id (int): The id of the company.

    Returns:
    - status_code (200): The company has been found successfully.
    - status_code (404): The company is not found.
    - status_code (400): The request is invalid.

    """
    status, status_code, response = service_company.get_company_by_id(db, id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create a new company.")
def create_company(
    address: str = Form(..., description="The address of the company."),
    email: str = Form(..., description="The email of the company."),
    name: str = Form(..., description="The name of the company."),
    phone_number: str = Form(..., description="The phone number of the company."),
    scale: str = Form(..., description="The scale of the company."),
    tax_code: str = Form(..., description="The tax code of the company."),
    type: str = Form(..., description="The type of the company."),
    fields: List[int] = Form(
        ..., description="The fields of the company.", example=[1, 2]
    ),
    logo: UploadFile = File(None, description="The logo of the company."),
    company_short_description: str = Form(
        None, description="The short description of the company."
    ),
    website: str = Form(None, description="The website of the company."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a new company.

    This endpoint allows creating a new company with the provided information.

    Parameters:
    - address (str): The address of the company.
    - email (str): The email address of the company.
    - name (str): The name of the company.
    - phone_number (str): The phone number of the company.
    - scale (str): The scale of the company.
    - tax_code (str): The tax code of the company.
    - type (str): The type of the company.
    - fields (list): The fields of the company.
    - logo (UploadFile): The logo of the company.
    - company_short_description (str): The short description of the company.
    - website (str): The website of the company.

    Returns:
    - status_code (201): The company has been created successfully.
    - status_code (401): The company is not authorized.
    - status_code (400): The request is invalid.
    - status_code (409): The company is already registered.

    """
    data = {k: v for k, v in locals().items() if k not in ["db"]}
    print(data)
    status, status_code, response = service_company.create_company(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update a user.")
def update_user(
    id: int = Path(..., description="The id of the user."),
    address: str = Form(None, description="The address of the company."),
    email: str = Form(None, description="The email of the company."),
    phone_number: str = Form(None, description="The phone number of the company."),
    scale: str = Form(None, description="The scale of the company."),
    tax_code: str = Form(None, description="The tax code of the company."),
    fields: list = Form(None, description="The fields of the company."),
    logo: UploadFile = File(None, description="The logo of the company."),
    company_short_description: str = Form(
        None, description="The short description of the company."
    ),
    website: str = Form(None, description="The website of the company."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update a company.

    This endpoint allows updating a company with the provided information,

    Parameters:
    - id (int): The id of the company.
    - address (str): The address of the company.
    - email (str): The email address of the company.
    - phone_number (str): The phone number of the company.
    - scale (str): The scale of the company.
    - tax_code (str): The tax code of the company.
    - fields (list): The fields of the company.
    - logo (UploadFile): The logo of the company.
    - company_short_description (str): The short description of the company.
    - website (str): The website of the company.

    Returns:
    - status_code (200): The company has been updated successfully.
    - status_code (401): company is not authorized.
    - status_code (400): The request is invalid.
    - status_code (404): The company is not found.

    """

    data = {k: v for k, v in locals().items() if k not in ["db"]}

    status, status_code, response = service_company.update_company(
        db, {"company_id": id, **data}, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete a company.")
def delete_company(
    id: int = Path(..., description="The id of the company.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete a company.

    This endpoint allows deleting a company by id.

    Parameters:
    - id (int): The id of the company.

    Returns:
    - status_code (200): The company has been deleted successfully.
    - status_code (401): User is not authorized.
    - status_code (404): The company is not found.

    """

    status, status_code, response = service_company.delete_company(db, id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
