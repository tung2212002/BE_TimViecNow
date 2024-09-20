from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    group_position as schema_group_position,
)
from app.core import constant
from app.core.job_position.job_position_hepler import job_position_helper


class JobPositionService:
    async def get_position(self, db: Session, data: dict):
        page = job_position_helper.validate_pagination(data)

        job_positions = crud.job_position.get_multi(db, **page.model_dump())

        job_positions_response = job_position_helper.get_list_info(db, job_positions)
        return constant.SUCCESS, 200, job_positions_response

    async def get_group(self, db: Session, data: dict):
        page = job_position_helper.validate_pagination(data)

        group_positions = crud.group_position.get_multi(db, **page.model_dump())

        group_position_response = [
            schema_group_position.GroupPositionItemResponse(
                **group_position.__dict__,
                tags=job_position_helper.get_list_info(db, group_position.job_positions)
            )
            for group_position in group_positions
        ]

        return constant.SUCCESS, 200, group_position_response

    async def get_position_by_id(self, db: Session, id: int):
        job_position = crud.job_position.get(db, id)
        if not job_position:
            return constant.ERROR, 404, "Job position not found"
        job_position_response = job_position_helper.get_info(db, job_position)
        return constant.SUCCESS, 200, job_position_response

    async def get_group_by_id(self, db: Session, id: int):
        group_position = crud.group_position.get(db, id)
        if not group_position:
            return constant.ERROR, 404, "Group position not found"
        group_position_response = schema_group_position.GroupPositionItemResponse(
            **group_position.__dict__,
            tags=job_position_helper.get_list_info(db, group_position.job_positions)
        )
        return constant.SUCCESS, 200, group_position_response

    async def create_position(self, db: Session, data: dict):
        job_position_data = job_position_helper.validate_create(data)

        id = job_position_data.id
        if not crud.group_position.get(db, id) or not id:
            return constant.ERROR, 404, "Group position not found"

        job_position = crud.job_position.create(db, obj_in=job_position_data)
        return constant.SUCCESS, 201, job_position

    async def create_group(self, db: Session, data: dict):
        group_position_data = job_position_helper.validate_position_group_create(data)

        group_position = crud.group_position.get_by_name(db, group_position_data.name)
        if group_position:
            return constant.ERROR, 409, "Group position already registered"

        group_position = crud.group_position.create(db, obj_in=group_position_data)
        return constant.SUCCESS, 201, group_position

    async def update_position(self, db: Session, id: int, data: dict):
        job_position = crud.job_position.get(db, id)
        if not job_position:
            return constant.ERROR, 404, "Job position not found"

        job_position_data = job_position_helper.validate_update(data)

        job_position = crud.job_position.update(
            db, db_obj=job_position, obj_in=job_position_data
        )
        return constant.SUCCESS, 200, job_position

    async def update_group(self, db: Session, id: int, data: dict):
        group_position = crud.group_position.get(db, id)
        if not group_position:
            return constant.ERROR, 404, "Group position not found"

        group_position_data = job_position_helper.validate_position_group_update(data)

        group_position = crud.group_position.update(
            db, db_obj=group_position, obj_in=group_position_data
        )
        return constant.SUCCESS, 200, group_position

    async def delete_position(self, db: Session, id: int):
        job_position = crud.job_position.get(db, id)
        if not job_position:
            return constant.ERROR, 404, "Job position not found"

        job_position = crud.job_position.remove(db, id=id)
        return constant.SUCCESS, 200, job_position

    async def delete_group(self, db: Session, id: int):
        group_position = crud.group_position.get(db, id)
        if not group_position:
            return constant.ERROR, 404, "Group position not found"

        group_position = crud.group_position.remove(db, id=id)
        return constant.SUCCESS, 200, group_position


job_position_service = JobPositionService()
