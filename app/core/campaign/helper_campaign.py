from sqlalchemy.orm import Session
from typing import Optional, Union
from pydantic import BaseModel
import json

from app.crud.campaign import campaign as campaignCRUD
from app.crud.company import company as companyCRUD
from app.crud.job import job as jobCRUD
from app.schema import (
    campaign as schema_campaign,
    job as schema_job,
)
from app.hepler.enum import Role, CampaignStatus
from app.core import constant
from app.hepler.response_custom import custom_response_error
from app.core.job import helper_job


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
    job = helper_job.get_job_info_general(db, campaign.job[0]) if campaign.job else None
    campaign_response = schema_campaign.CampaignItemResponse(
        **{k: v for k, v in campaign.__dict__.items() if k not in ["job"]},
        job=job.model_dump() if job else None,
    )
    return campaign_response


def get_list_campaign(db: Session, page: Union[dict, BaseModel]):
    multi_paigination = schema_campaign.CampaignGetMutilPagination(**page.model_dump())
    # multi_paigination = schema_campaign.CampaignGetMutilPagination(**page.model_dump())
    count_pagination = schema_campaign.CountGetListPagination(**page.model_dump())
    print(multi_paigination)
    return campaignCRUD.get_multi(
        db, **multi_paigination.model_dump()
    ), campaignCRUD.count(db, **count_pagination.model_dump())


def get_list_campaign_open(db: Session, page: Union[dict, BaseModel]):
    page = schema_campaign.CampaignGetOnlyOpenPagination(**page.model_dump())
    return campaignCRUD.get_multi(db, **page.model_dump()), campaignCRUD.count(
        db, **page.model_dump()
    )


def get_list_campaign_has_new_application(db: Session, page: Union[dict, BaseModel]):
    page = schema_campaign.CampaignGetHasNewApplicationPagination(**page.model_dump())
    return campaignCRUD.get_multi(db, **page.model_dump()), campaignCRUD.count(db, **{})


def get_list_campaign_has_published_job(db: Session, page: Union[dict, BaseModel]):
    page = schema_campaign.CampaignGetHasPublishedJobPagination(**page.model_dump())
    return campaignCRUD.get_has_published_job(
        db, **page.model_dump()
    ), campaignCRUD.count(db, **page.model_dump())


def get_list_campaign_has_published_job_expired(
    db: Session, page: Union[dict, BaseModel]
):
    page = schema_campaign.CampaignGetHasPublishedJobExpiredPagination(
        **page.model_dump()
    )
    return campaignCRUD.get_has_published_job(
        db, **page.model_dump()
    ), campaignCRUD.count(db, **page.model_dump())


def get_list_campaign_has_pending_job(db: Session, page: Union[dict, BaseModel]):
    page = schema_campaign.CampaignGetHasPendingJobPagination(**page.model_dump())
    return campaignCRUD.get_has_pending_job(
        db, **page.model_dump()
    ), campaignCRUD.count(db, **page.model_dump())
