from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app.crud import (
    job_position as job_positionCRUD,
    group_position as group_positionCRUD,
)
from app.schema.group_position import (
    GroupPositionCreateRequest,
    GroupPositionUpdateRequest,
    GroupPositionItemResponse,
)
from app.schema.page import Pagination
from app.schema.job_position import JobPositionCreateRequest, JobPositionUpdateRequest
from app.core.job_position.job_position_hepler import job_position_helper
from fastapi import status
from app.common.exception import CustomException
from app.common.response import CustomResponse
from app.storage.cache.config_cache_service import config_cache_service


class JobPositionService:
    async def get_position(self, db: Session, redis: Redis, data: dict):
        page = Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await config_cache_service.get_cache_position(redis, key)
        except Exception as e:
            print(e)

        if not response:
            job_positions = job_positionCRUD.get_multi(db, **page.model_dump())
            response = [
                job_position_helper.get_info(db, job_position)
                for job_position in job_positions
            ]
            try:
                await config_cache_service.cache_position(redis, key, response)
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_group(self, db: Session, redis: Redis, data: dict):
        page = Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await config_cache_service.get_cache_position_group(redis, key)
        except Exception as e:
            print(e)

        if not response:
            group_positions = group_positionCRUD.get_multi(db, **page.model_dump())
            response = [
                GroupPositionItemResponse(
                    **group_position.__dict__,
                    tags=job_position_helper.get_list_info(
                        db, group_position.job_positions
                    )
                )
                for group_position in group_positions
            ]
            try:
                await config_cache_service.cache_position_group(redis, key, response)
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_position_by_id(self, db: Session, id: int):
        job_position = job_positionCRUD.get(db, id)
        if not job_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Job position not found"
            )

        response = job_position_helper.get_info(db, job_position)

        return CustomResponse(data=response)

    async def get_group_by_id(self, db: Session, id: int):
        group_position = group_positionCRUD.get(db, id)
        if not group_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        response = GroupPositionItemResponse(
            **group_position.__dict__,
            tags=job_position_helper.get_list_info(db, group_position.job_positions)
        )

        return CustomResponse(data=response)

    async def create_position(self, db: Session, data: dict):
        job_position_data = JobPositionCreateRequest(**data)

        id = job_position_data.id
        if not group_positionCRUD.get(db, id) or not id:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        response = job_positionCRUD.create(db, obj_in=job_position_data)

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def create_group(self, db: Session, data: dict):
        group_position_data = GroupPositionCreateRequest(**data)

        group_position = group_positionCRUD.get_by_name(db, group_position_data.name)
        if group_position:
            raise CustomException(
                status_code=status.HTTP_409_CONFLICT,
                msg="Group position already registered",
            )

        response = group_positionCRUD.create(db, obj_in=group_position_data)

        return CustomResponse(status_code=status.HTTP_201_CREATED, data=response)

    async def update_position(self, db: Session, id: int, data: dict):
        job_position = job_positionCRUD.get(db, id)
        if not job_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Job position not found"
            )

        job_position_data = JobPositionUpdateRequest(**data)

        response = job_positionCRUD.update(
            db, db_obj=job_position, obj_in=job_position_data
        )

        return CustomResponse(data=response)

    async def update_group(self, db: Session, id: int, data: dict):
        group_position = group_positionCRUD.get(db, id)
        if not group_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        group_position_data = GroupPositionUpdateRequest(**data)

        response = group_positionCRUD.update(
            db, db_obj=group_position, obj_in=group_position_data
        )

        return CustomResponse(data=response)

    async def delete_position(self, db: Session, id: int):
        job_position = job_positionCRUD.get(db, id)
        if not job_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Job position not found"
            )

        job_positionCRUD.remove(db, id=id)

        return CustomResponse(msg="Deleted position successfully")

    async def delete_group(self, db: Session, id: int):
        group_position = group_positionCRUD.get(db, id)
        if not group_position:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Group position not found"
            )

        group_positionCRUD.remove(db, id=id)

        return CustomResponse(msg="Deleted group successfully")


job_position_service = JobPositionService()
