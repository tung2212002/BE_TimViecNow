from sqlalchemy.orm import Session
from typing import Optional, Union
from pydantic import BaseModel

from app import crud
from app.hepler.enum import CampaignStatus
from app.core.job.job_helper import job_helper
from app.model import Campaign
from app.schema.campaign import (
    CampaignItemResponse,
    CampaignGetMutilPagination,
    CountGetListPagination,
    CampaignGetOnlyOpenPagination,
    CampaignGetHasNewApplicationPagination,
    CampaignGetHasPublishedJobPagination,
    CampaignGetHasPublishedJobExpiredPagination,
    CampaignGetHasPendingJobPagination,
)
from fastapi import status as status_code
from app.common.exception import CustomException


class CampaignHelper:
    def check_exist(
        self,
        db: Session,
        business_id: int,
        campaign_id: Optional[int],
        status: Optional[CampaignStatus],
        title: str,
    ) -> Campaign:
        if campaign_id:
            campaign = crud.campaign.get(db, campaign_id)
            if not campaign:
                raise CustomException(
                    status_code=status_code.HTTP_404_NOT_FOUND, msg="Campaign not found"
                )

            if campaign.business_id != business_id:
                raise CustomException(
                    status_code=status_code.HTTP_403_FORBIDDEN, msg="Permission denied"
                )

            if campaign.status != status:
                raise CustomException(
                    status_code=status_code.HTTP_400_BAD_REQUEST,
                    msg="Campaign is not active",
                )

            return campaign
        else:
            company = crud.company.get_by_business_id(db, business_id)
            campaign = crud.campaign.create(
                db,
                obj_in={
                    "business_id": business_id,
                    "title": title,
                    "company_id": company.id,
                },
            )

            return campaign

    def get_info(self, db: Session, campaign: Campaign) -> CampaignItemResponse:
        job = job_helper.get_info_general(campaign.job[0]) if campaign.job else None
        campaign_response = CampaignItemResponse(
            **{k: v for k, v in campaign.__dict__.items() if k not in ["job"]},
            job=job.model_dump() if job else None,
        )

        return campaign_response

    def get_list_campaign(self, db: Session, page: Union[dict, BaseModel]):
        multi_paigination = CampaignGetMutilPagination(**page.model_dump())
        count_pagination = CountGetListPagination(**page.model_dump())

        return crud.campaign.get_multi(
            db, **multi_paigination.model_dump()
        ), crud.campaign.count(db, **count_pagination.model_dump())

    def get_list_campaign_open(self, db: Session, page: Union[dict, BaseModel]):
        page = CampaignGetOnlyOpenPagination(**page.model_dump())

        return crud.campaign.get_multi(db, **page.model_dump()), crud.campaign.count(
            db, **page.model_dump()
        )

    def get_list_campaign_has_new_application(
        db: Session, page: Union[dict, BaseModel]
    ):
        page = CampaignGetHasNewApplicationPagination(**page.model_dump())

        return crud.campaign.get_multi(db, **page.model_dump()), crud.campaign.count(
            db, **{}
        )

    def get_list_campaign_has_published_job(
        self, db: Session, page: Union[dict, BaseModel]
    ):
        page = CampaignGetHasPublishedJobPagination(**page.model_dump())

        return crud.campaign.get_has_published_job(
            db, **page.model_dump()
        ), crud.campaign.count(db, **page.model_dump())

    def get_list_campaign_has_published_job_expired(
        db: Session, page: Union[dict, BaseModel]
    ):
        page = CampaignGetHasPublishedJobExpiredPagination(**page.model_dump())

        return crud.campaign.get_has_published_job(
            db, **page.model_dump()
        ), crud.campaign.count(db, **page.model_dump())

    def get_list_campaign_has_pending_job(
        self, db: Session, page: Union[dict, BaseModel]
    ):
        page = CampaignGetHasPendingJobPagination(**page.model_dump())

        return crud.campaign.get_has_pending_job(
            db, **page.model_dump()
        ), crud.campaign.count(db, **page.model_dump())


campaign_helper = CampaignHelper()
