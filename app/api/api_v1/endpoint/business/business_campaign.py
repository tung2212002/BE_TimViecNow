from fastapi import APIRouter, Depends, Query, Path, Body

from app.db.base import CurrentSession
from app.core import constant
from app.core.campaign.campaign_service import campaign_service
from app.core.auth.user_manager_service import user_manager_service
from app.hepler.response_custom import custom_response_error, custom_response
from app.hepler.enum import FilterCampaign, OrderType, SortBy

router = APIRouter()


@router.get("", summary="Get list of campaign.")
async def get_campaign(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
    skip: int = Query(None, description="The number of users to skip.", example=0),
    limit: int = Query(None, description="The number of users to return.", example=10),
    sort_by: SortBy = Query(
        None, description="The field to sort by.", example=SortBy.ID
    ),
    order_by: OrderType = Query(
        None, description="The order to sort by.", example=OrderType.DESC
    ),
    business_id: int = Query(None, description="The business id.", example=1),
    company_id: int = Query(None, description="The company id.", example=1),
    filter_by: FilterCampaign = Query(
        None, description="The filter by.", example=FilterCampaign.ONLY_OPEN
    ),
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
    - company_id (int): The company id.
    - filter_by (str): The filter to filter by.

    Returns:
    - status_code (200): The list of campaign has been found successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.

    """
    args = locals()

    status_message, status_code, response = campaign_service.get(db, args, current_user)

    if status_message == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status_message == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.get("/{id}", summary="Get campaign by id.")
async def get_campaign_by_id(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
    id: int = Path(description="The campaign id.", example=1),
):
    """
    Get campaign by id.

    This endpoint allows getting a campaign by id.

    Parameters:
    - id (int): The campaign id.

    Returns:
    - status_code (200): The campaign has been found successfully.
    - status_code (403): The permission is denied.
    - status_code (404): The campaign is not found.

    """
    status, status_code, response = await campaign_service.get_by_id(
        db, id, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.post("", summary="Create campaign.")
async def create_campaign(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_business),
    data: dict = Body(
        ...,
        description="The campaign data.",
        example={
            "title": "Tuyển dụng nhân viên",
            "is_flash": False,
        },
    ),
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
    status, status_code, response = await campaign_service.create(
        db, data, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.put("/{id}", summary="Update campaign.")
async def update_campaign(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_business),
    id: int = Path(description="The campaign id.", example=1),
    data: dict = Body(
        ...,
        description="The campaign data.",
        example={
            "title": "Tuyển dụng nhân viên",
            "is_flash": False,
        },
    ),
):
    """
    Update campaign.

    This endpoint allows updating a campaign.

    Parameters:
    - id (int): The campaign id.
    - title (str): The title of the campaign.
    - is_flash (bool): The campaign is flash.

    Returns:
    - status_code (200): The campaign has been updated successfully.
    - status_code (400): The request is invalid.
    - status_code (403): The permission is denied.
    - status_code (404): The campaign is not found.

    """
    status, status_code, response = await campaign_service.update(
        db, {**data, "id": id}, current_user
    )

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)


@router.delete("/{id}", summary="Delete campaign.")
async def delete_campaign(
    db: CurrentSession,
    current_user=Depends(user_manager_service.get_current_business_admin_superuser),
    id: int = Path(description="The campaign id.", example=1),
):
    """
    Delete campaign.

    This endpoint allows deleting a campaign.

    Parameters:
    - id (int): The campaign id.

    Returns:
    - status_code (200): The campaign has been deleted successfully.
    - status_code (403): The permission is denied.
    - status_code (404): The campaign is not found.

    """
    status, status_code, response = await campaign_service.delete(db, id, current_user)

    if status == constant.ERROR:
        return custom_response_error(status_code, constant.ERROR, response)
    elif status == constant.SUCCESS:
        return custom_response(status_code, constant.SUCCESS, response)
