from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path,
    Form,
    File,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.core import constant
from app.core.company import service_company
from app.core.auth.service_business_auth import get_current_user, get_current_business
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import OrderType, SortBy, CompanyType


router = APIRouter()


@router.get("", summary="Get list of company.")
def get_company(
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=10),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: str = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    business_id: int = Query(None, description="The business id.", example=1),
    keyword: str = Query(None, description="The keyword.", example="cong ty"),
    fields: list[int] = Query(
        None, description="The list of field id.", example=list([int(2)])
    ),
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
    - keyword (str): The keyword.
    - fields (list[int]): The list of field id.

    Returns:
    - status_code (200): The list of company has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = locals()
    status_message, status_code, response = service_company.get(db, args, current_user)

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
    status, status_code, response = service_company.get_by_id(db, company_id)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create company.")
def create_company(
    name: str = Form(
        ...,
        description="The name of the company.",
        json_schema_extra={"example": "Công ty Giáo dục ABC"},
    ),
    email: str = Form(
        ...,
        description="The email of the company.",
        json_schema_extra={"example": "congtyabc@hust.edu.vn"},
    ),
    phone_number: str = Form(
        ...,
        description="The phone number of the company.",
        json_schema_extra={"example": "0323456789"},
    ),
    address: str = Form(
        ...,
        description="The address of the company.",
        json_schema_extra={"example": "1 Dai Co Viet, Hai Ba Trung, Ha Noi"},
    ),
    website: str = Form(
        ...,
        description="The website of the company.",
        json_schema_extra={"example": "https://congtyabc.com"},
    ),
    scale: str = Form(
        ...,
        description="The scale of the company.",
        json_schema_extra={"example": "100-499"},
    ),
    tax_code: str = Form(
        ...,
        description="The tax code of the company.",
        json_schema_extra={"example": "1234567890"},
    ),
    type: CompanyType = Form(
        ...,
        description="The type of the company.",
        json_schema_extra={"example": CompanyType.COMPANY},
    ),
    company_short_description: str = Form(
        None,
        description="The short description of the company.",
        json_schema_extra={"example": "Công ty giáo dục hàng đầu Việt Nam"},
    ),
    fields: list[int] = Form(
        ...,
        description="The list of field id.",
        json_schema_extra={"example": list([int(2)])},
    ),
    logo: UploadFile = File(None, description="The logo of the company."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_business),
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
    data = locals()

    status, status_code, response = service_company.create(db, data, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{company_id}", summary="Update company.")
def update_company(
    company_id: int = Path(description="The company id.", example=1),
    email: str = Form(
        None,
        description="The email of the company.",
        json_schema_extra={"example": "congtyabc@hust.edu.vn"},
    ),
    phone_number: str = Form(
        None,
        description="The phone number of the company.",
        json_schema_extra={"example": "0323456789"},
    ),
    address: str = Form(
        None,
        description="The address of the company.",
        json_schema_extra={"example": "1 Dai Co Viet, Hai Ba Trung, Ha Noi"},
    ),
    website: str = Form(
        None,
        description="The website of the company.",
        json_schema_extra={"example": "https://congtyabc.com"},
    ),
    scale: str = Form(
        None,
        description="The scale of the company.",
        json_schema_extra={"example": "100-499"},
    ),
    tax_code: str = Form(
        None,
        description="The tax code of the company.",
        json_schema_extra={"example": "1234567890"},
    ),
    type: CompanyType = Form(
        None,
        description="The type of the company.",
        json_schema_extra={"example": CompanyType.COMPANY},
    ),
    company_short_description: str = Form(
        None,
        description="The short description of the company.",
        json_schema_extra={"example": "Công ty giáo dục hàng đầu Việt Nam"},
    ),
    fields: list[int] = Form(
        None,
        description="The list of field id.",
        json_schema_extra={"example": list([int(2)])},
    ),
    logo: UploadFile = File(None, description="The logo of the company."),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_business),
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
    - type (CompanyType): The type of the company.
    - company_short_description (str): The short description of the company.
    - fields (list[int]): The list of field id.
    - logo (UploadFile): The logo of the company.

    Returns:
    - status_code (200): The company has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The company is not found.

    """
    data = locals()
    status, status_code, response = service_company.update(
        db,
        {**data},
        current_user,
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

    status, status_code, response = service_company.delete(db, id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
