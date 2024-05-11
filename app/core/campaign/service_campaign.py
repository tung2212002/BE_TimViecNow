from sqlalchemy.orm import Session
from typing import Optional

from app.crud.campaign import campaign as campaignCRUD
from app.crud.company import company as companyCRUD
from app.core.job import service_job
from app.core.auth import service_business_auth
from app.schema import (
    campaign as schema_campaign,
)
from app.hepler.enum import Role, CampaignStatus
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def get(db: Session, data: dict, current_user):
    try:
        page = schema_campaign.CampaignGetListPagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    campaigns = []
    business_id = page.business_id
    role = service_business_auth.check_permission_business(
        current_user,
        roles=[Role.BUSINESS, Role.ADMIN, Role.SUPER_USER],
        business_id=business_id,
    )
    if role == Role.BUSINESS:
        business = current_user.business
        company = business.company
        if not company:
            return constant.ERROR, 404, "Business not join any company"
        if (business_id and business_id != business.id) or (
            page.company_id and page.company_id != company.id
        ):
            return constant.ERROR, 403, "Permission denied"
        page.business_id = business_id
        page.company_id = company.id
        campaigns = campaignCRUD.get_multi(db, **page.model_dump())
        count_pagination = schema_campaign.CountGetListPagination(**page.model_dump())
        count = campaignCRUD.count(
            db,
            **count_pagination.model_dump(),
        )
    else:
        campaigns = campaignCRUD.get_multi(db, **page.model_dump())
        count = campaignCRUD.count(
            db, **schema_campaign.CountGetListPagination(**data).model_dump()
        )
    campaigns_response = [get_campaign_info(db, campaign) for campaign in campaigns]
    return constant.SUCCESS, 200, {"count": count, "campaigns": campaigns_response}


def get_by_id(db: Session, campaign_id: int, current_user):
    campaign = campaignCRUD.get(db, campaign_id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    company = companyCRUD.get_company_by_business_id(db, current_user.id)
    if current_user.role == Role.BUSINESS and (
        campaign.business_id != current_user.id
        or not company
        or campaign.company_id != company.id
    ):

        return constant.ERROR, 403, "Permission denied"
    campaign_response = get_campaign_info(db, campaign)
    return constant.SUCCESS, 200, campaign_response


def create(db: Session, data: dict, current_user):
    try:
        campaign_data = schema_campaign.CampaignCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    if current_user.role == Role.BUSINESS:
        business = current_user.business
        company = business.company
        if not company:
            return constant.ERROR, 404, "Business not join any company"
        business = current_user.business
        campaign_data = {
            **campaign_data.model_dump(),
            "business_id": business.id,
            "company_id": company.id,
        }
    campaign = campaignCRUD.create(db, obj_in=campaign_data)
    campaign_response = get_campaign_info(db, campaign)
    return constant.SUCCESS, 201, campaign_response


def update(db: Session, data: dict, current_user):
    campaign_id = data.get("id")
    campaign = campaignCRUD.get(db, campaign_id)
    company = companyCRUD.get_company_by_business_id(db, current_user.id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    if current_user.role == Role.BUSINESS and (
        campaign.business_id != current_user.id
        or not company
        or company.id != campaign.company_id
    ):
        return constant.ERROR, 403, "Permission denied"
    try:
        campaign_data = schema_campaign.CampaignUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    campaign = campaignCRUD.update(db, db_obj=campaign, obj_in=campaign_data)
    campaign_response = get_campaign_info(db, campaign)
    return constant.SUCCESS, 200, campaign_response


def delete(db: Session, id: int, current_user):
    campaign = campaignCRUD.get(db, id)
    company = companyCRUD.get_company_by_business_id(db, current_user.id)
    if not campaign:
        return constant.ERROR, 404, "Campaign not found"
    if current_user.role == Role.BUSINESS and (
        campaign.business_id != current_user.id
        or not company
        or company.id != campaign.company_id
    ):
        return constant.ERROR, 403, "Permission denied"
    campaign = campaignCRUD.remove(db, id=id)
    return constant.SUCCESS, 200, "Campaign has been deleted"


def check_campaign_exist(
    db: Session,
    business_id: int,
    campaign_id: Optional[int],
    status: Optional[CampaignStatus],
    title: str,
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
        if campaign.status != status:
            return custom_response_error(
                status_code=400,
                status=constant.ERROR,
                response="Campaign is not active",
            )
        return campaign
    else:
        company = companyCRUD.get_company_by_business_id(db, business_id)
        campaign = campaignCRUD.create(
            db,
            obj_in={
                "business_id": business_id,
                "title": title,
                "company_id": company.id,
            },
        )
        return campaign


def get_campaign_info(db: Session, campaign):
    job = (
        service_job.get_job_info_general(db, campaign.job[0]) if campaign.job else None
    )
    campaign_response = schema_campaign.CampaignItemResponse(
        **{k: v for k, v in campaign.__dict__.items() if k not in ["job"]},
        job=job.model_dump() if job else None,
    )
    return campaign_response
