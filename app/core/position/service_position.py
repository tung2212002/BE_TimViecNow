from sqlalchemy.orm import Session

from app.crud.job_position import job_position as job_positionCRUD
from app.crud.group_position import group_position as group_positionCRUD
from app.schema import (
    job_position as schema_job_position,
    group_position as schema_group_position,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error


def get_position(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    job_positions = job_positionCRUD.get_multi(db, **page.model_dump())

    job_positions_response = [
        schema_job_position.JobPositionItemResponse(**job_position.__dict__)
        for job_position in job_positions
    ]
    return constant.SUCCESS, 200, job_positions_response


def get_group(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    group_positions = group_positionCRUD.get_multi(db, **page.model_dump())

    group_position_response = [
        schema_group_position.GroupPositionItemResponse(
            **group_position.__dict__,
            tags=[
                schema_job_position.JobPositionItemResponse(**tag.__dict__)
                for tag in group_position.job_positions
            ]
        )
        for group_position in group_positions
    ]

    return constant.SUCCESS, 200, group_position_response


def get_position_by_id(db: Session, id: int):
    job_position = job_positionCRUD.get(db, id)
    if not job_position:
        return constant.ERROR, 404, "Job position not found"
    job_position_response = schema_job_position.JobPositionItemResponse(
        **job_position.__dict__
    )
    return constant.SUCCESS, 200, job_position_response


def get_group_by_id(db: Session, id: int):
    group_position = group_positionCRUD.get(db, id)
    if not group_position:
        return constant.ERROR, 404, "Group position not found"
    group_position_response = schema_group_position.GroupPositionItemResponse(
        **group_position.__dict__,
        tags=[
            schema_job_position.JobPositionItemResponse(**tag.__dict__)
            for tag in group_position.job_positions
        ]
    )
    return constant.SUCCESS, 200, group_position_response


def create_position(db: Session, data: dict):
    try:
        job_position_data = schema_job_position.JobPositionCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    id = job_position_data.id
    if not group_positionCRUD.get(db, id) or not id:
        return constant.ERROR, 404, "Group position not found"

    job_position = job_positionCRUD.create(db, obj_in=job_position_data)
    return constant.SUCCESS, 201, job_position


def create_group(db: Session, data: dict):
    try:
        group_position_data = schema_group_position.GroupPositionCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    group_position = group_positionCRUD.get_by_name(db, group_position_data.name)
    if group_position:
        return constant.ERROR, 409, "Group position already registered"

    group_position = group_positionCRUD.create(db, obj_in=group_position_data)
    return constant.SUCCESS, 201, group_position


def update_position(db: Session, id: int, data: dict):
    job_position = job_positionCRUD.get(db, id)
    if not job_position:
        return constant.ERROR, 404, "Job position not found"

    try:
        job_position_data = schema_job_position.JobPositionUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    job_position = job_positionCRUD.update(
        db, db_obj=job_position, obj_in=job_position_data
    )
    return constant.SUCCESS, 200, job_position


def update_group(db: Session, id: int, data: dict):
    group_position = group_positionCRUD.get(db, id)
    if not group_position:
        return constant.ERROR, 404, "Group position not found"

    try:
        group_position_data = schema_group_position.GroupPositionUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    group_position = group_positionCRUD.update(
        db, db_obj=group_position, obj_in=group_position_data
    )
    return constant.SUCCESS, 200, group_position


def delete_position(db: Session, id: int):
    job_position = job_positionCRUD.get(db, id)
    if not job_position:
        return constant.ERROR, 404, "Job position not found"

    job_position = job_positionCRUD.remove(db, id=id)
    return constant.SUCCESS, 200, job_position


def delete_group(db: Session, id: int):
    group_position = group_positionCRUD.get(db, id)
    if not group_position:
        return constant.ERROR, 404, "Group position not found"

    group_position = group_positionCRUD.remove(db, id=id)
    return constant.SUCCESS, 200, group_position
