from sqlalchemy.orm import Session
from typing import Optional, Union
from pydantic import BaseModel

from app import crud
from app.schema import (
    campaign as schema_campaign,
)
from app.hepler.enum import CampaignStatus
from app.core import constant
from app.hepler.response_custom import custom_response_error
from app.core.job.job_helper import job_helper
from app.model import Campaign
from app.core.helper_base import HelperBase

# def check_campaign_exist(
#     db: Session,
#     business_id: int,
#     campaign_id: Optional[int],
#     status: Optional[CampaignStatus],
#     title: str,
# ):
#     if campaign_id:
#         campaign = crud.campaign.get(db, campaign_id)
#         if not campaign:
#             return custom_response_error(
#                 status_code=404, status=constant.ERROR, response="Campaign not found"
#             )
#         if campaign.business_id != business_id:
#             return custom_response_error(
#                 status_code=403, status=constant.ERROR, response="Permission denied"
#             )
#         if campaign.status != status:
#             return custom_response_error(
#                 status_code=400,
#                 status=constant.ERROR,
#                 response="Campaign is not active",
#             )
#         return campaign
#     else:
#         company = crud.company.get_by_business_id(db, business_id)
#         campaign = crud.campaign.create(
#             db,
#             obj_in={
#                 "business_id": business_id,
#                 "title": title,
#                 "company_id": company.id,
#             },
#         )
#         return campaign


# def get_campaign_info(self, db: Session, campaign):
#     job = job_helper.get_job_info_general(db, campaign.job[0]) if campaign.job else None
#     campaign_response = schema_campaign.CampaignItemResponse(
#         **{k: v for k, v in campaign.__dict__.items() if k not in ["job"]},
#         job=job.model_dump() if job else None,
#     )
#     return campaign_response


# def get_list_campaign(self, db: Session, page: Union[dict, BaseModel]):
#     multi_paigination = schema_campaign.CampaignGetMutilPagination(**page.model_dump())
#     count_pagination = schema_campaign.CountGetListPagination(**page.model_dump())
#     return crud.campaign.get_multi(
#         db, **multi_paigination.model_dump()
#     ), crud.campaign.count(db, **count_pagination.model_dump())


# def get_list_campaign_open(self, db: Session, page: Union[dict, BaseModel]):
#     page = schema_campaign.CampaignGetOnlyOpenPagination(**page.model_dump())
#     return crud.campaign.get_multi(db, **page.model_dump()), crud.campaign.count(
#         db, **page.model_dump()
#     )


# def get_list_campaign_has_new_application(self, db: Session, page: Union[dict, BaseModel]):
#     page = schema_campaign.CampaignGetHasNewApplicationPagination(**page.model_dump())
#     return crud.campaign.get_multi(db, **page.model_dump()), crud.campaign.count(
#         db, **{}
#     )


# def get_list_campaign_has_published_job(self, db: Session, page: Union[dict, BaseModel]):
#     page = schema_campaign.CampaignGetHasPublishedJobPagination(**page.model_dump())
#     return crud.campaign.get_has_published_job(
#         db, **page.model_dump()
#     ), crud.campaign.count(db, **page.model_dump())


# def get_list_campaign_has_published_job_expired(
#     db: Session, page: Union[dict, BaseModel]
# ):
#     page = schema_campaign.CampaignGetHasPublishedJobExpiredPagination(
#         **page.model_dump()
#     )
#     return crud.campaign.get_has_published_job(
#         db, **page.model_dump()
#     ), crud.campaign.count(db, **page.model_dump())


# def get_list_campaign_has_pending_job(self, db: Session, page: Union[dict, BaseModel]):
#     page = schema_campaign.CampaignGetHasPendingJobPagination(**page.model_dump())
#     return crud.campaign.get_has_pending_job(
#         db, **page.model_dump()
#     ), crud.campaign.count(db, **page.model_dump())


class CampaignHelper(HelperBase):
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
                return custom_response_error(
                    status_code=404,
                    status=constant.ERROR,
                    response="Campaign not found",
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

    def get_info(
        self, db: Session, campaign: Campaign
    ) -> schema_campaign.CampaignItemResponse:
        job = job_helper.get_info_general(db, campaign.job[0]) if campaign.job else None
        campaign_response = schema_campaign.CampaignItemResponse(
            **{k: v for k, v in campaign.__dict__.items() if k not in ["job"]},
            job=job.model_dump() if job else None,
        )
        return campaign_response

    def get_list_campaign(self, db: Session, page: Union[dict, BaseModel]):
        multi_paigination = schema_campaign.CampaignGetMutilPagination(
            **page.model_dump()
        )
        count_pagination = schema_campaign.CountGetListPagination(**page.model_dump())
        return crud.campaign.get_multi(
            db, **multi_paigination.model_dump()
        ), crud.campaign.count(db, **count_pagination.model_dump())

    def get_list_campaign_open(self, db: Session, page: Union[dict, BaseModel]):
        page = schema_campaign.CampaignGetOnlyOpenPagination(**page.model_dump())
        return crud.campaign.get_multi(db, **page.model_dump()), crud.campaign.count(
            db, **page.model_dump()
        )

    def get_list_campaign_has_new_application(
        db: Session, page: Union[dict, BaseModel]
    ):
        page = schema_campaign.CampaignGetHasNewApplicationPagination(
            **page.model_dump()
        )
        return crud.campaign.get_multi(db, **page.model_dump()), crud.campaign.count(
            db, **{}
        )

    def get_list_campaign_has_published_job(
        self, db: Session, page: Union[dict, BaseModel]
    ):
        page = schema_campaign.CampaignGetHasPublishedJobPagination(**page.model_dump())
        return crud.campaign.get_has_published_job(
            db, **page.model_dump()
        ), crud.campaign.count(db, **page.model_dump())

    def get_list_campaign_has_published_job_expired(
        db: Session, page: Union[dict, BaseModel]
    ):
        page = schema_campaign.CampaignGetHasPublishedJobExpiredPagination(
            **page.model_dump()
        )
        return crud.campaign.get_has_published_job(
            db, **page.model_dump()
        ), crud.campaign.count(db, **page.model_dump())

    def get_list_campaign_has_pending_job(
        self, db: Session, page: Union[dict, BaseModel]
    ):
        page = schema_campaign.CampaignGetHasPendingJobPagination(**page.model_dump())
        return crud.campaign.get_has_pending_job(
            db, **page.model_dump()
        ), crud.campaign.count(db, **page.model_dump())


campaign_helper = CampaignHelper(
    schema_campaign.CampaignGetListPagination,
    schema_campaign.CampaignCreateRequest,
    schema_campaign.CampaignUpdateRequest,
)
