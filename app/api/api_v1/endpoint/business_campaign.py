from fastapi import APIRouter, Depends, Query, Path, Body, Request
from sqlalchemy.orm import Session
from typing import List

from app.db.base import get_db
from app.core import constant
from app.core.campaign import service_campaign
from app.core.auth.service_business_auth import get_current_user, get_current_admin
from app.hepler.response_custom import custom_response_error, custom_response

router = APIRouter()


@router.get("", summary="Get list of campaign.")
def get_campaign(
    request: Request,
    skip: int = Query(0, description="The number of users to skip.", example=0),
    limit: int = Query(100, description="The number of users to return.", example=100),
    sort_by: str = Query("id", description="The field to sort by.", example="id"),
    order_by: str = Query("asc", description="The order to sort by.", example="asc"),
    business_id: int = Query(None, description="The business id.", example=1),
    status: str = Query(1, description="The status of campaign.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get list of campaign.

    This endpoint allows getting a list of campaign.

    Parameters:
    - skip (int): The number of users to skip.
    - limit (int): The number of users to return.
    - sort_by (str): The field to sort by.
    - order_by (str): The order to sort by.
    - business_id (int): The business id.
    - status (int): The status of campaign.

    Returns:
    - status_code (200): The list of campaign has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = {item[0]: item[1] for item in request.query_params.multi_items()}

    status_message, status_code, response = service_campaign.get_list_campaign(
        db, {**args}, current_user
    )

    if status_message == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status_message == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{campaign_id}", summary="Get campaign by id.")
def get_campaign_by_id(
    campaign_id: int = Path(description="The campaign id.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get campaign by id.

    This endpoint allows getting a campaign by id.

    Parameters:
    - campaign_id (int): The campaign id.

    Returns:
    - status_code (200): The campaign has been found successfully.
    - status_code (403): The permission is denied.
    - status_code (404): The campaign is not found.

    """
    status, status_code, response = service_campaign.get_campaign_by_id(
        db, campaign_id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create campaign.")
def create_campaign(
    data: dict = Body(
        ...,
        description="The campaign data.",
        example={
            "title": "Tuyển dụng nhân viên",
            "is_flash": False,
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create campaign.

    This endpoint allows creating a campaign.

    Parameters:
    - title (str): The title of the campaign.
    - is_flash (bool): The campaign is flash.

    Returns:
    - status_code (201): The campaign has been created successfully.
    - status_code (400): The request is invalid.

    """
    status, status_code, response = service_campaign.create_campaign(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{campaign_id}", summary="Update campaign.")
def update_campaign(
    campaign_id: int = Path(description="The campaign id.", example=1),
    data: dict = Body(
        ...,
        description="The campaign data.",
        example={
            "title": "Tuyển dụng nhân viên",
            "is_flash": False,
        },
    ),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Update campaign.

    This endpoint allows updating a campaign.

    Parameters:
    - campaign_id (int): The campaign id.
    - title (str): The title of the campaign.
    - is_flash (bool): The campaign is flash.

    Returns:
    - status_code (200): The campaign has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The campaign is not found.

    """
    status, status_code, response = service_campaign.update_campaign(
        db, {**data, "campaign_id": campaign_id}, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{campaign_id}", summary="Delete campaign.")
def delete_campaign(
    campaign_id: int = Path(description="The campaign id.", example=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Delete campaign.

    This endpoint allows deleting a campaign.

    Parameters:
    - campaign_id (int): The campaign id.

    Returns:
    - status_code (200): The campaign has been deleted successfully.
    - status_code (403): The permission is denied.
    - status_code (404): The campaign is not found.

    """
    status, status_code, response = service_campaign.delete_campaign(
        db, campaign_id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
