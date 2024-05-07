from sqlalchemy.orm import Session
from typing import Optional

from app.crud.campaign import campaign as campaignCRUD
from app.core.job import service_job
from app.core.auth import service_business_auth
from app.schema import (
    page as schema_page,
    campaign as schema_campaign,
    job as schema_job,
)
from app.hepler.enum import Role, CampaignStatus
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def get_list_campaign(db: Session, data: dict, current_user):
    try:
        page = schema_campaign.CampaignGetListPagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    campaigns = []
    business_id = data.get("business_id")
    role = service_business_auth.check_permission_business(
        current_user,
        roles=[Role.BUSINESS, Role.ADMIN, Role.SUPER_USER],
        business_id=business_id,
    )
    # if not business_id and current_user.role == Role.BUSINESS:
    #     business_id = current_user.business.id
    #     campaigns = campaignCRUD.get_multi(db, business_id=business_id, **page.dict())
    # elif (
    #     not business_id and current_user.role not in [Role.SUPER_USER, Role.ADMIN]
    # ) or (
    #     business_id
    #     and (
    #         current_user.role != Role.SUPER_USER
    #         or (
    #             current_user.business.id != business_id
    #             and current_user.role not in [Role.ADMIN]
    #         )
    #     )
    # ):
    #     return constant.ERROR, 403, "Permission denied"
    # elif business_id:
    #     campaigns = campaignCRUD.get_multi_by_business_id(
    #         db, business_id, **page.dict()
    #     )
    # else:
    #     campaigns = campaignCRUD.get_multi(db, **page.dict())
    # if role == Role.BUSINESS:
    #     campaigns = campaignCRUD.get_multi_by_business_id(
    #         db, business_id, **page.dict()
    #     )

    # else:
    campaigns = campaignCRUD.get_multi(db, **page.dict())
    count = campaignCRUD.count(
        db, **schema_campaign.CountGetListPagination(**data).dict()
    )
    campaigns_response = [get_campaign_info(db, campaign) for campaign in campaigns]
    return constant.SUCCESS, 200, {"count": count, "campaigns": campaigns_response}


def get_campaign_by_id(db: Session, campaign_id: int, current_user):
    campaign = campaignCRUD.get(db, campaign_id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    if (
        current_user.role == Role.BUSINESS
        and campaign.business_id != current_user.business.id
    ):
        return constant.ERROR, 403, "Permission denied"
    campaign_response = get_campaign_info(db, campaign)
    return constant.SUCCESS, 200, campaign_response


def create_campaign(db: Session, data: dict, current_user):
    try:
        campaign_data = schema_campaign.CampaignCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    if current_user.role == Role.BUSINESS:
        campaign_data = {
            **campaign_data.dict(),
            "business_id": current_user.business.id,
        }
    campaign = campaignCRUD.create(db, obj_in=campaign_data)
    campaign_response = get_campaign_info(db, campaign)
    return constant.SUCCESS, 201, campaign_response


def check_campaign_exist(
    db: Session, business_id: int, campaign_id: Optional[int], title: str
):
    if campaign_id:
        campaign = campaignCRUD.get(db, campaign_id)
        if not campaign:
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="Campaign not found"
            )
        if campaign.business_id != business_id:
            return custom_response_error(
                status_code=403, status=constant.ERROR, response="Permission denied"
            )
        if campaign.status != CampaignStatus.OPEN:
            return custom_response_error(
                status_code=400, status=constant.ERROR, response="Campaign is not open"
            )
        return campaign
    else:
        campaign = campaignCRUD.create(
            db, obj_in={"business_id": business_id, "title": title}
        )
        return campaign


def update_campaign(db: Session, data: dict, current_user):
    campaign_id = data.get("campaign_id")
    campaign = campaignCRUD.get(db, campaign_id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    if (
        current_user.role == Role.BUSINESS
        and campaign.business_id != current_user.business.id
    ):
        return constant.ERROR, 403, "Permission denied"
    try:
        campaign_data = schema_campaign.CampaignUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    campaign = campaignCRUD.update(db, db_obj=campaign, obj_in=campaign_data)
    campaign_response = get_campaign_info(db, campaign)
    return constant.SUCCESS, 200, campaign_response


def delete_campaign(db: Session, campaign_id: int, current_user):
    campaign = campaignCRUD.get(db, campaign_id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    if (
        current_user.role == Role.BUSINESS
        and campaign.business_id != current_user.business.id
    ):
        return constant.ERROR, 403, "Permission denied"
    campaign = campaignCRUD.remove(db, id=campaign_id)
    return constant.SUCCESS, 200, "Campaign has been deleted"


def get_campaign_info(db: Session, campaign):
    job = (
        service_job.get_job_info_general(db, campaign.job[0]) if campaign.job else None
    )
    campaign_response = schema_campaign.CampaignItemResponse(
        **{k: v for k, v in campaign.__dict__.items() if k not in ["job"]},
        job=job.dict() if job else None,
    )
    return campaign_response
