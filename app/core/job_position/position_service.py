from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app import crud
from app.schema import (
    group_position as schema_group_position,
    page as schema_page,
    job_position as schema_job_position,
)
from app.core.job_position.job_position_hepler import job_position_helper
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse
from app.storage.cache.config_cache_service import config_cache_service


class JobPositionService:
    async def get_position(self, db: Session, redis: Redis, data: dict):
        page = schema_page.Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await config_cache_service.get_cache_position(redis, key)
        except Exception as e:
            print(e)

        if not response:
            job_positions = crud.job_position.get_multi(db, **page.model_dump())
            response = [
                job_position_helper.get_info(db, job_position)
                for job_position in job_positions
            ]
            try:
                await config_cache_service.cache_position(
                    redis, key, [job_position.__dict__ for job_position in response]
                )
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_group(self, db: Session, redis: Redis, data: dict):
        page = schema_page.Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await config_cache_service.get_cache_group(redis, key)
        except Exception as e:
            print(e)

        if not response:
            group_positions = crud.group_position.get_multi(db, **page.model_dump())
            response = [
                schema_group_position.GroupPositionItemResponse(
                    **group_position.__dict__,
                    tags=job_position_helper.get_list_info(
                        db, group_position.job_positions
                    )
                )
                for group_position in group_positions
            ]
            try:
                await config_cache_service.cache_group(
                    redis, key, [group_position.__dict__ for group_position in response]
                )
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_position_by_id(self, db: Session, id: int):
        job_position = crud.job_position.get(db, id)
        if not job_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Job position not found"
            )

        response = job_position_helper.get_info(db, job_position)

        return CustomResponse(data=response)

    async def get_group_by_id(self, db: Session, id: int):
        group_position = crud.group_position.get(db, id)
        if not group_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        response = schema_group_position.GroupPositionItemResponse(
            **group_position.__dict__,
            tags=job_position_helper.get_list_info(db, group_position.job_positions)
        )

        return CustomResponse(data=response)

    async def create_position(self, db: Session, data: dict):
        job_position_data = schema_job_position.JobPositionCreateRequest(**data)

        id = job_position_data.id
        if not crud.group_position.get(db, id) or not id:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        response = crud.job_position.create(db, obj_in=job_position_data)

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def create_group(self, db: Session, data: dict):
        group_position_data = schema_group_position.GroupPositionCreateRequest(**data)

        group_position = crud.group_position.get_by_name(db, group_position_data.name)
        if group_position:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT,
                msg="Group position already registered",
            )

        response = crud.response.create(db, obj_in=group_position_data)

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def update_position(self, db: Session, id: int, data: dict):
        job_position = crud.job_position.get(db, id)
        if not job_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Job position not found"
            )

        job_position_data = schema_job_position.JobPositionUpdateRequest(**data)

        response = crud.job_position.update(
            db, db_obj=job_position, obj_in=job_position_data
        )

        return CustomResponse(data=response)

    async def update_group(self, db: Session, id: int, data: dict):
        group_position = crud.group_position.get(db, id)
        if not group_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        group_position_data = schema_group_position.GroupPositionUpdateRequest(**data)

        response = crud.group_position.update(
            db, db_obj=group_position, obj_in=group_position_data
        )

        return CustomResponse(data=response)

    async def delete_position(self, db: Session, id: int):
        job_position = crud.job_position.get(db, id)
        if not job_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Job position not found"
            )

        crud.job_position.remove(db, id=id)

        return CustomResponse(msg="Deleted position successfully")

    async def delete_group(self, db: Session, id: int):
        group_position = crud.group_position.get(db, id)
        if not group_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        crud.group_position.remove(db, id=id)

        return CustomResponse(msg="Deleted group successfully")


job_position_service = JobPositionService()
