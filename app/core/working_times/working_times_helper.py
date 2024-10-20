from fastapi import status
from sqlalchemy.orm import Session
from typing import List

from app.crud import working_time as working_timeCRUD
from app.schema.working_time import (
    WorkingTimeCreate,
    WorkingTimeResponse,
    WorkingTimeUpdate,
    WorkingTimeCreateRequest,
)
from app.common.exception import CustomException


class WorkingTimesHelper:
    def get_by_job_id(self, db: Session, job_id: int) -> List[dict]:
        working_times = working_timeCRUD.get_by_job_id(db, job_id)

        return [
            WorkingTimeResponse(**working_time.__dict__).model_dump()
            for working_time in working_times
        ]

    def get_by_id(self, db: Session, id: int) -> dict:
        working_time = working_timeCRUD.get(db, id)
        if not working_time:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg="Working time not found",
            )

        return WorkingTimeResponse(**working_time.__dict__).model_dump()

    def get_by_ids(self, db: Session, ids: List[int]) -> List[dict]:
        working_times = [self.get_by_id(db, id) for id in ids]

        return working_times

    def check_list_valid(self, db: Session, working_times: List[dict]) -> List[dict]:
        if working_times is None or not working_times:
            return []

        for working_time in working_times:
            WorkingTimeCreateRequest(**working_time)

        return working_times

    def create(self, db: Session, data: dict) -> dict:
        working_time_data = WorkingTimeCreate(**data).model_dump()

        working_time = working_timeCRUD.create(db, obj_in=working_time_data)

        return WorkingTimeResponse(**working_time.__dict__).model_dump()

    def update(self, db: Session, id: int, data: dict) -> dict:
        working_time = working_timeCRUD.get(db, id)
        if not working_time:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg="Working time not found",
            )

        working_time_data = WorkingTimeUpdate(**data).model_dump()

        working_time = working_timeCRUD.update(
            db, db_obj=working_time, obj_in=working_time_data
        )

        return WorkingTimeResponse(**working_time.__dict__).model_dump()

    def delete(self, db: Session, id: int) -> None:
        working_time = working_timeCRUD.get(db, id)
        if not working_time:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg="Working time not found",
            )

        working_timeCRUD.remove(db, id)

    def create_with_job_id(
        self, db: Session, job_id: int, data: List[dict]
    ) -> List[dict]:
        working_times = []
        for working_time in data:
            working_time_data = WorkingTimeCreate(
                job_id=job_id, **working_time
            ).model_dump()

            working_time = working_timeCRUD.create(db, obj_in=working_time_data)
            working_times.append(
                WorkingTimeResponse(**working_time.__dict__).model_dump()
            )

        return working_times

    def update_with_job_id(
        self, db: Session, job_id: int, new_working_times: List[dict]
    ) -> List[dict]:
        working_timeCRUD.remove_by_job_id(db, job_id)
        working_times = []
        for working_time in new_working_times:
            working_time_in = WorkingTimeCreate(
                job_id=job_id, **working_time
            ).model_dump()
            working_time = working_timeCRUD.create(db, obj_in=working_time_in)
            working_times.append(
                WorkingTimeResponse(**working_time.__dict__).model_dump()
            )

        return working_times

    def delete_with_job_id(self, db: Session, job_id: int) -> None:
        working_timeCRUD.remove_by_job_id(db, job_id)


working_times_helper = WorkingTimesHelper()
