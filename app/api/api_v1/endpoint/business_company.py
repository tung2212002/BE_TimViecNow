from fastapi import APIRouter, Depends, Query, Path, Body, Request
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.core import constant
from app.core.company import service_company
from app.core.auth.service_business_auth import get_current_user, get_current_admin
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("", summary="Get list of company.")
def get_company(
    request: Request,
    skip: int = Query(0, description="The number of users to skip.", example=0),
    limit: int = Query(100, description="The number of users to return.", example=100),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
    business_id: int = Query(None, description="The business id.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get list of company.

    This endpoint allows getting a list of company.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - business_id (int): The business id.

    Returns:
    - status_code (200): The list of company has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status_message, status_code, response = service_company.get_list_company(
        db, {**args}, current_user
    )

    if status_message == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status_message == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{company_id}", summary="Get company by id.")
def get_company_by_id(
    company_id: int = Path(description="The company id.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get company by id.

    This endpoint allows getting a company by id.

    Parameters:
    - company_id (int): The company id.

    Returns:
    - status_code (200): The company has been found successfully.
    - status_code (404): The company is not found.

    """
    status, status_code, response = service_company.get_company_by_id(
        db, company_id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create company.")
def create_company(
    data: dict = Body(
        ...,
        description="The company data.",
        example={
            "name": "Công ty Giáo dục ABC",
            "email": "congtyabc@hust.edu.vn",
            "phone_number": "0123456789",
            "address": "1 Dai Co Viet, Hai Ba Trung, Ha Noi",
            "website": "https://congtyabc.com",
            "scale": "100-499",
            "tax_code": "1234567890",
            "company_short_description": "Công ty giáo dục hàng đầu Việt Nam",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create company.

    This endpoint allows creating a company.

    Parameters:
    - title (str): The title of the company.
    - is_flash (bool): The company is flash.

    Returns:
    - status_code (201): The company has been created successfully.
    - status_code (400): The request is invalid.

    """
    status, status_code, response = service_company.create_company(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{company_id}", summary="Update company.")
def update_company(
    company_id: int = Path(description="The company id.", example=1),
    data: dict = Body(
        ...,
        description="The company data.",
        example={
            "name": "Công ty Giáo dục ABC (update)",
            "email": "congtyabc@hust.edu.vn",
            "phone_number": "0123456789",
            "address": "1 Dai Co Viet, Hai Ba Trung, Ha Noi (update)",
            "website": "https://congtyabc.com",
            "scale": "100-499",
            "tax_code": "1234567890",
            "company_short_description": "Công ty giáo dục hàng đầu Việt Nam (update)",
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update company.

    This endpoint allows updating a company.

    Parameters:
    - company_id (int): The company id.
    - name (str): The name of the company.
    - email (str): The email of the company.
    - phone_number (str): The phone number of the company.
    - address (str): The address of the company.
    - website (str): The website of the company.
    - scale (str): The scale of the company.
    - tax_code (str): The tax code of the company.
    - company_short_description (str): The short description of the company.

    Returns:
    - status_code (200): The company has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The company is not found.

    """
    status, status_code, response = service_company.update_company(
        db, {**data, "company_id": company_id}, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
