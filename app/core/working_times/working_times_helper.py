from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud
from app.schema import working_time as working_time_schema
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.model import WorkingTime
from app.core.helper_base import HelperBase


class WorkingTimesHelper(HelperBase):
    def get_by_job_id(self, db: Session, job_id: int) -> List[dict]:
        working_times = crud.working_time.get_by_job_id(db, job_id)
        return [
            working_time_schema.WorkingTimeResponse(
                **working_time.__dict__
            ).model_dump()
            for working_time in working_times
        ]

    def get_by_id(self, db: Session, id: int) -> dict:
        working_time = crud.working_time.get(db, id)
        if not working_time:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response="Working time not found",
            )

        return working_time_schema.WorkingTimeResponse(
            **working_time.__dict__
        ).model_dump()

    def get_by_ids(self, db: Session, ids: List[int]) -> List[dict]:
        working_times = [self.get_by_id(db, id) for id in ids]
        return working_times

    def check_list_valid(self, db: Session, working_times: List[dict]) -> List[dict]:
        if working_times is None or not working_times:
            return []

        try:
            [
                working_time_schema.WorkingTimeCreateRequest(**working_time)
                for working_time in working_times
            ]
        except Exception as e:
            return custom_response_error(
                status=400, response=get_message_validation_error(e)
            )
        return working_times

    def create(self, db: Session, data: dict) -> dict:
        try:
            working_time_data = working_time_schema.WorkingTimeCreate(
                **data
            ).model_dump()
        except Exception as e:
            return custom_response_error(
                status=400, response=get_message_validation_error(e)
            )

        working_time = crud.working_time.create(db, obj_in=working_time_data)
        return working_time_schema.WorkingTimeResponse(
            **working_time.__dict__
        ).model_dump()

    def update(self, db: Session, id: int, data: dict) -> dict:
        working_time = crud.working_time.get(db, id)
        if not working_time:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response="Working time not found",
            )

        try:
            working_time_data = working_time_schema.WorkingTimeUpdate(
                **data
            ).model_dump()
        except Exception as e:
            return custom_response_error(
                status=400, response=get_message_validation_error(e)
            )

        working_time = crud.working_time.update(
            db, db_obj=working_time, obj_in=working_time_data
        )
        return working_time_schema.WorkingTimeResponse(
            **working_time.__dict__
        ).model_dump()

    def delete(self, db: Session, id: int) -> None:
        working_time = crud.working_time.get(db, id)
        if not working_time:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response="Working time not found",
            )

        crud.working_time.remove(db, id)

    def create_with_job_id(
        self, db: Session, job_id: int, data: List[dict]
    ) -> List[dict]:
        working_times = []
        for working_time in data:
            try:
                working_time_data = working_time_schema.WorkingTimeCreate(
                    job_id=job_id, **working_time
                ).model_dump()
            except Exception as e:
                return custom_response_error(
                    status=400, response=get_message_validation_error(e)
                )
            working_time = crud.working_time.create(db, obj_in=working_time_data)
            working_times.append(
                working_time_schema.WorkingTimeResponse(
                    **working_time.__dict__
                ).model_dump()
            )
        return working_times

    def update_with_job_id(
        self, db: Session, job_id: int, new_working_times: List[dict]
    ) -> List[dict]:
        crud.working_time.remove_by_job_id(db, job_id)
        working_times = []
        for working_time in new_working_times:
            working_time_in = working_time_schema.WorkingTimeCreate(
                job_id=job_id, **working_time
            ).model_dump()
            working_time = crud.working_time.create(db, obj_in=working_time_in)
            working_times.append(
                working_time_schema.WorkingTimeResponse(
                    **working_time.__dict__
                ).model_dump()
            )
        return working_times

    def delete_with_job_id(self, db: Session, job_id: int) -> None:
        crud.working_time.remove_by_job_id(db, job_id)


working_times_helper = WorkingTimesHelper(
    None,
    working_time_schema.WorkingTimeCreateRequest,
    working_time_schema.WorkingTimeUpdate,
)
