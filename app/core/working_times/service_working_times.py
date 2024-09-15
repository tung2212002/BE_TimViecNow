from sqlalchemy.orm import Session

from app.crud.working_time import working_time as working_timeCRUD
from app.schema import working_time as working_time_schema
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def get_working_times_by_job_id(db: Session, job_id: int):
    working_times = working_timeCRUD.get_working_times_by_job_id(db, job_id=job_id)
    return [
        working_time_schema.WorkingTimeResponse(**working_time.__dict__).model_dump()
        for working_time in working_times
    ]


def get_working_time(db: Session, working_time_id: int):
    working_time = working_timeCRUD.get(db, working_time_id)
    if not working_time:
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Working time not found"
        )

    return working_time_schema.WorkingTimeResponse(**working_time.__dict__).model_dump()


def get_working_time_by_id(db: Session, working_time_id: int):
    working_time = working_timeCRUD.get(db, working_time_id)
    if not working_time:
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Working time not found"
        )

    return working_time


def get_working_times_by_ids(db: Session, working_time_ids: list):
    working_times = [
        get_working_time_by_id(db, working_time_id)
        for working_time_id in working_time_ids
    ]
    return working_times


def check_working_times(db: Session, woking_times: list):
    if woking_times is None:
        return True

    for working_time in woking_times:
        try:
            working_time_data = working_time_schema.WorkingTimeCreateRequest(
                **working_time
            ).model_dump()
        except Exception as e:
            return custom_response_error(
                status=400, response=get_message_validation_error(e)
            )
    return True


def create_working_time(db: Session, data: dict):
    try:
        working_time_data = working_time_schema.WorkingTimeCreate(**data)
    except Exception as e:
        return custom_response_error(
            status_code=400,
            status=constant.ERROR,
            response=get_message_validation_error(e),
        )

    working_time = working_timeCRUD.create(db=db, obj_in=working_time_data)
    return working_time


def create_working_time_job(db: Session, job_id: int, data: list):
    working_times = []
    for working_time in data:
        try:
            working_time_data = working_time_schema.WorkingTimeCreate(
                job_id=job_id, **working_time
            )
        except Exception as e:
            return custom_response_error(
                status=400, response=get_message_validation_error(e)
            )
    for working_time in data:
        working_time = working_timeCRUD.create(db=db, obj_in=working_time_data)
        working_times.append(working_time)
    return working_times


def update_working_time(db: Session, working_time_id: int, data: dict):
    working_time = working_timeCRUD.get(db, working_time_id)
    if not working_time:
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Working time not found"
        )

    try:
        working_time_data = working_time_schema.WorkingTimeUpdate(**data)
    except Exception as e:
        return custom_response_error(
            status_code=400,
            status=constant.ERROR,
            response=get_message_validation_error(e),
        )

    working_time = working_timeCRUD.update(
        db=db, db_obj=working_time, obj_in=working_time_data
    )
    return working_time


def update_working_time_job(
    db: Session, job_id: int, new_working_times: list, working_times: list
):
    for working_time in working_times:
        working_time = working_timeCRUD.remove(db, id=working_time.id)
    working_times = []
    for working_time in new_working_times:
        working_time_in = working_time_schema.WorkingTimeCreate(
            job_id=job_id, **working_time
        )
        working_time = working_timeCRUD.create(db=db, obj_in=working_time_in)
        working_times.append(working_time)
    return working_times


def delete_working_time(db: Session, working_time_id: int):
    working_time = working_timeCRUD.get(db, working_time_id)
    if not working_time:
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Working time not found"
        )

    working_time = working_timeCRUD.remove(db, id=working_time_id)
    return working_time
