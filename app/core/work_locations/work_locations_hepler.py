from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.schema import (
    work_location as work_location_schema,
    province as schema_province,
    district as schema_district,
)
from app.core import constant
from app.core.location.location_helper import location_helper
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.model import WorkLocation
from app.core.helper_base import HelperBase


class WorkLocationHepler(HelperBase):
    def get_by_job_id(self, db: Session, job_id: int) -> List[dict]:
        work_locations = crud.work_location.get_by_job_id(db, job_id)
        work_locations_response = []
        for work_location in work_locations:
            work_locations_response.append(self.get_info(db, work_location))
        return work_locations_response

    def get_by_id(self, db: Session, id: int) -> dict:
        work_location = crud.work_location.get(db, id)
        if not work_location:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response="Working time not found",
            )

        return self.get_info(db, work_location)

    def get_by_ids(self, db: Session, ids: List[int]) -> List[dict]:
        work_locations = [self.get_by_id(db, id) for id in ids]
        return work_locations

    def create_with_job_id(
        self, db: Session, job_id: int, data: List[dict]
    ) -> List[dict]:
        return [
            self.create(
                db,
                work_location_schema.WorkLocatioCreate(job_id=job_id, **work_location),
            )
            for work_location in data
        ]

    def create(self, db: Session, data: work_location_schema.WorkLocatioCreate) -> dict:
        work_location = crud.work_location.create(db, data)
        return self.get_info(db, work_location)

    def update_with_job_id(
        self, db: Session, job_id: int, data: List[dict]
    ) -> List[dict]:
        crud.work_location.remove_by_job_id(db, job_id)
        return [
            self.update(
                db,
                work_location_schema.WorkLocatioUpdate(job_id=job_id, **work_location),
            )
            for work_location in data
        ]

    def update(self, db: Session, id: int, data: dict) -> dict:
        work_location = crud.work_location.get(db, id)
        if not work_location:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response="Working time not found",
            )

        work_location = crud.work_location.update(db, work_location, data)
        return self.get_info(db, work_location)

    def delete(self, db: Session, id: int) -> None:
        work_location = crud.work_location.get(db, id)
        if not work_location:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response="Working time not found",
            )

        work_location = crud.work_location.remove(db, id)
        return work_location

    def get_info(self, db: Session, work_location: WorkLocation) -> dict:
        province = crud.province.get(db, work_location.province_id)
        district = crud.district.get(db, work_location.district_id)
        work_location_response = work_location_schema.WorkLocatioResponse(
            **work_location.__dict__,
            province=(
                {
                    **schema_province.ProvinceItemResponse(
                        **province.__dict__
                    ).model_dump(),
                }
                if province
                else None
            ),
            district=(
                {
                    **schema_district.DistrictItemResponse(
                        **district.__dict__
                    ).model_dump(),
                }
                if district
                else None
            ),
        )
        return work_location_response

    def check_valid(self, db: Session, data: dict) -> dict:
        if not data:
            return data
        location_helper.check_valid_province_district(
            db, data["province_id"], data["district_id"]
        )
        return data

    def check_list_valid(self, db: Session, data: List[dict]) -> List[dict]:
        if not data or data is None:
            return data
        return [self.check_valid(db, province_district) for province_district in data]


work_location_helper = WorkLocationHepler(
    None,
    work_location_schema.WorkLocatioCreateRequest,
    work_location_schema.WorkLocatioUpdateRequest,
)
