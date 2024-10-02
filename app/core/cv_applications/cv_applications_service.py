from sqlalchemy.orm import Session
from redis.asyncio import Redis
from typing import List
from fastapi import status

from app import crud
from app.schema import (
    job as schema_job,
    cv_application as schema_cv_application,
)
from app.common.exception import CustomException
from app.model import CVApplication, User, Business, ManagerBase
from app.common.response import CustomResponse
from app.storage.cache.cv_cache_service import cv_cache_service
from app.core.cv_applications.cv_applications_helper import cv_applications_helper
from app.storage.s3 import s3_service
from app.core.cv_applications.cv_applications_helper import cv_applications_helper


class CVApplicationsService:
    async def get(
        self, db: Session, redis: Redis, data: dict, current_user: User
    ) -> CustomResponse:
        page = schema_cv_application.CVApplicationUserFilter(**data)
        count_page = schema_cv_application.CVApplicationUserFilterCount(**data)
        key = page.get_key(current_user.id)

        count = crud.cv_applications.count_by_user_id(
            db, user_id=current_user.id, **count_page.model_dump()
        )

        if count < page.skip:
            return CustomResponse(data={"jobs": [], "count": count})

        cv_applications = crud.cv_applications.get_by_user_id(
            db, user_id=current_user.id, **page.model_dump()
        )

        cv_applications_response = [
            await cv_applications_helper.get_full_info(db, cv_application)
            for cv_application in cv_applications
        ]

        return CustomResponse(data={"jobs": cv_applications_response, "count": count})

    async def get_by_id(
        self, db: Session, id: int, current_user: User
    ) -> CustomResponse:
        cv_application = crud.cv_applications.get(db, id)

        if not cv_application:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="CV application not found"
            )

        if cv_application.user_id != current_user.id:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN, msg="Forbidden"
            )

        response = await cv_applications_helper.get_full_info(db, cv_application)

        return CustomResponse(data=response)

    async def create(
        self, db: Session, redis: Redis, data: dict, current_user: User
    ) -> CustomResponse:
        cv_applications_data = schema_cv_application.CVApplicationCreateRequest(**data)

        job = cv_applications_helper.job_open(db, cv_applications_data.job_id)
        if not job:
            raise CustomException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, msg="Job is not open"
            )

        cv_application = crud.cv_applications.get_by_user_id_and_campaign_id(
            db, user_id=current_user.id, campaign_id=job.campaign.id
        )
        if cv_application:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT,
                msg="CV application already exists",
            )

        cv_file = cv_applications_data.cv
        if cv_file:
            key = cv_file.filename
            s3_service.upload_file(cv_file, key)
            cv_applications_data.cv = key

        obj_in = schema_cv_application.CVApplicationCreate(
            **cv_applications_data.__dict__,
            user_id=current_user.id,
            campaign_id=job.campaign.id,
        )
        cv_application = crud.cv_applications.create(db, obj_in=obj_in)
        crud.campaign.increase_count_apply(db, job.campaign)
        crud.user.increase_count_job_apply(db, current_user)

        try:
            await cv_cache_service.incr(
                redis, f"{current_user.id}_{cv_application.status}"
            )
        except Exception as e:
            print(e)

        response = await cv_applications_helper.get_full_info(db, cv_application)

        return CustomResponse(data=response)

    async def update(
        self, db: Session, data: dict, current_user: ManagerBase
    ) -> CustomResponse:
        cv_application_data = schema_cv_application.CVApplicationUpdateRequest(**data)

        cv_application = crud.cv_applications.get(
            db, cv_application_data.cv_application_id
        )
        if not cv_application:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="CV application not found"
            )

        if cv_application.campaign.business_id != current_user.id:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN, msg="Forbidden"
            )

        cv_application = crud.cv_applications.update(
            db,
            db_obj=cv_application,
            obj_in=schema_cv_application.CVApplicationUpdate(
                **cv_application_data.model_dump()
            ),
        )

        response = await cv_applications_helper.get_full_info(db, cv_application)

        return CustomResponse(data=response)


cv_applications_service = CVApplicationsService()
