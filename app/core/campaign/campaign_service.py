from sqlalchemy.orm import Session
from typing import Optional

from app.crud.campaign import campaign as campaignCRUD
from app.crud.company import company as companyCRUD
from app.core.job import job_service, job_helper
from app.core.auth import business_auth_service
from app.schema import (
    campaign as schema_campaign,
)
from app.hepler.enum import Role, CampaignStatus, FilterCampaign
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.model import ManagerBase, Campaign
from app.core.campaign.campaign_helper import campaign_helper


filter_functions = {
    None: lambda db, page: campaign_helper.get_list_campaign(db, page),
    FilterCampaign.ONLY_OPEN: lambda db, page: campaign_helper.get_list_campaign_open(
        db, page
    ),
    FilterCampaign.HAS_NEW_CV: lambda db, page: campaign_helper.get_list_campaign_has_new_application(
        db, page
    ),
    FilterCampaign.HAS_PUBLISHING_JOB: lambda db, page: campaign_helper.get_list_campaign_has_published_job(
        db, page
    ),
    FilterCampaign.EXPIRED_JOB: lambda db, page: campaign_helper.get_list_campaign_has_published_job_expired(
        db, page
    ),
    FilterCampaign.WAITING_APPROVAL_JOB: lambda db, page: campaign_helper.get_list_campaign_has_pending_job(
        db, page
    ),
}


# async def get(db: Session, data: dict, current_user):
#     try:
#         page = schema_campaign.CampaignGetListPagination(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     campaigns = []
#     business_id = page.business_id
#     role = business_auth_service.check_permission_business(
#         current_user,
#         roles=[Role.BUSINESS, Role.ADMIN, Role.SUPER_USER],
#         business_id=business_id,
#     )
#     if role == Role.BUSINESS:
#         business = current_user.business
#         company = business.company
#         if not company:
#             return constant.ERROR, 404, "Business not join any company"
#         if (business_id and business_id != business.id) or (
#             page.company_id and page.company_id != company.id
#         ):
#             return constant.ERROR, 403, "Permission denied"
#         page.business_id = business_id
#         page.company_id = company.id
#         # campaigns = campaignCRUD.get_multi(db, **page.model_dump())
#         # count_pagination = schema_campaign.CountGetListPagination(**page.model_dump())
#         # count = campaignCRUD.count(
#         #     db,
#         #     **count_pagination.model_dump(),
#         # )

#         # campaigns = campaignCRUD.get_multi(db, **page.model_dump())
#         # count = campaignCRUD.count(
#         #     db, **schema_campaign.CountGetListPagination(**data).model_dump()
#         # )
#     # count_in = schema_campaign.CountGetListPagination(**data)
#     # count = campaignCRUD.count(
#     #     db,
#     #     **count_in.model_dump(),
#     # )
#     campaigns, count = filter_functions.get(page.filter_by)(db, page)
#     campaigns_response = [
#         get_campaign_info(db, campaign) for campaign in campaigns
#     ]
#     return constant.SUCCESS, 200, {"count": count, "campaigns": campaigns_response}


# async def get_by_id(db: Session, campaign_id: int, current_user):
#     campaign = campaignCRUD.get(db, campaign_id)
#     if not campaign:
#         return constant.ERROR, 404, "Campaign not found"
#     company = companyCRUD.get_by_business_id(db, current_user.id)
#     if current_user.role == Role.BUSINESS and (
#         campaign.business_id != current_user.id
#         or not company
#         or campaign.company_id != company.id
#     ):

#         return constant.ERROR, 403, "Permission denied"
#     campaign_response = get_campaign_info(db, campaign)
#     return constant.SUCCESS, 200, campaign_response


# async def create(db: Session, data: dict, current_user):
#     try:
#         campaign_data = schema_campaign.CampaignCreateRequest(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     if current_user.role == Role.BUSINESS:
#         business = current_user.business
#         company = business.company
#         if not company:
#             return constant.ERROR, 404, "Business not join any company"
#         business = current_user.business
#         campaign_data = {
#             **campaign_data.model_dump(),
#             "business_id": business.id,
#             "company_id": company.id,
#         }
#     campaign = campaignCRUD.create(db, obj_in=campaign_data)
#     campaign_response = get_campaign_info(db, campaign)
#     return constant.SUCCESS, 201, campaign_response


# async def update(db: Session, data: dict, current_user):
#     campaign_id = data.get("id")
#     campaign = campaignCRUD.get(db, campaign_id)
#     company = companyCRUD.get_by_business_id(db, current_user.id)
#     if not campaign:
#         return constant.ERROR, 404, "Campaign not found"
#     if current_user.role == Role.BUSINESS and (
#         campaign.business_id != current_user.id
#         or not company
#         or company.id != campaign.company_id
#     ):
#         return constant.ERROR, 403, "Permission denied"
#     try:
#         campaign_data = schema_campaign.CampaignUpdateRequest(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     campaign = campaignCRUD.update(db, db_obj=campaign, obj_in=campaign_data)
#     campaign_response = get_campaign_info(db, campaign)
#     return constant.SUCCESS, 200, campaign_response


# async def delete(db: Session, id: int, current_user):
#     campaign = campaignCRUD.get(db, id)
#     company = companyCRUD.get_by_business_id(db, current_user.id)
#     if not campaign:
#         return constant.ERROR, 404, "Campaign not found"
#     if current_user.role == Role.BUSINESS and (
#         campaign.business_id != current_user.id
#         or not company
#         or company.id != campaign.company_id
#     ):
#         return constant.ERROR, 403, "Permission denied"
#     campaign = campaignCRUD.remove(db, id=id)
#     return constant.SUCCESS, 200, "Campaign has been deleted"


class CampaignService:
    async def get(self, db: Session, data: dict, current_user: ManagerBase):
        page = campaign_helper.validate_pagination(data)

        campaigns = []
        business_id = page.business_id
        role = business_auth_service.check_permission_business(
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
                page.company_id
                and page.company_id != company.id
                or page.company_id != company.id
            ):
                return constant.ERROR, 403, "Permission denied"
            page.business_id = business_id
            page.company_id = company.id
            campaigns, count = filter_functions.get(page.filter_by)(db, page)
        campaigns_response = [
            campaign_helper.get_info(db, campaign) for campaign in campaigns
        ]
        return constant.SUCCESS, 200, {"count": count, "campaigns": campaigns_response}

    async def get_list(self, db: Session, data: dict):
        page = schema_campaign.CampaignGetListPagination(**data)

        campaigns = filter_functions.get(page.filter_by)(db, page)
        campaigns_response = [
            campaign_helper.get_info(db, campaign) for campaign in campaigns
        ]
        return constant.SUCCESS, 200, {"campaigns": campaigns_response}

    async def get_by_id(self, db: Session, campaign_id: int, current_user: ManagerBase):
        campaign = campaignCRUD.get(db, campaign_id)
        if not campaign:
            return constant.ERROR, 404, "Campaign not found"
        company = companyCRUD.get_by_business_id(db, current_user.id)
        if current_user.role == Role.BUSINESS and (
            campaign.business_id != current_user.id
            or not company
            or campaign.company_id != company.id
        ):
            return constant.ERROR, 403, "Permission denied"
        campaign_response = campaign_helper.get_info(db, campaign)
        return constant.SUCCESS, 200, campaign_response

    async def create(self, db: Session, data: dict, current_user: ManagerBase):
        campaign_data = campaign_helper.validate_create(data)

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
        campaign_response = campaign_helper.get_info(db, campaign)
        return constant.SUCCESS, 201, campaign_response

    async def update(self, db: Session, data: dict, current_user: ManagerBase):
        campaign_id = data.get("id")
        campaign = campaignCRUD.get(db, campaign_id)
        company = companyCRUD.get_by_business_id(db, current_user.id)
        if not campaign:
            return constant.ERROR, 404, "Campaign not found"
        if current_user.role == Role.BUSINESS and (
            campaign.business_id != current_user.id
            or not company
            or company.id != campaign.company_id
        ):
            return constant.ERROR, 403, "Permission denied"
        campaign_data = campaign_helper.validate_update(data)

        campaign = campaignCRUD.update(db, db_obj=campaign, obj_in=campaign_data)
        campaign_response = campaign_helper.get_info(db, campaign)
        return constant.SUCCESS, 200, campaign_response

    async def delete(self, db: Session, id: int, current_user: ManagerBase):
        campaign = campaignCRUD.get(db, id)
        company = companyCRUD.get_by_business_id(db, current_user.id)
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


campaign_service = CampaignService()
