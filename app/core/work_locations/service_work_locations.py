from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.work_location import work_location as work_locationCRUD
from app.crud.province import province as provinceCRUD
from app.crud.district import district as districtCRUD
from app.model.work_location import WorkLocation
from app.schema import (
    work_location as work_location_schema,
    province as schema_province,
    district as schema_district,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def get_work_locations_by_job_id(db: Session, job_id: int):
    work_locations = work_locationCRUD.get_work_locations_by_job_id(db, job_id=job_id)
    work_locations_response = []
    for work_location in work_locations:
        work_location = get_work_location_by_work_location_id(db, work_location)
        work_locations_response.append(work_location)
    return work_locations_response


def get_work_location_by_id(db: Session, work_location_id: int):
    work_location = work_locationCRUD.get(db, work_location_id)
    if not work_location:
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Working time not found"
        )

    work_location_response = get_work_location_by_work_location_id(db, work_location)
    return work_location_response


def get_work_location_by_work_location_id(db: Session, work_location):
    province = provinceCRUD.get(db, work_location.province_id)
    district = districtCRUD.get(db, work_location.district_id)
    work_location_response = work_location_schema.WorkLocatioResponse(
        **work_location.__dict__,
        province=(
            {
                **schema_province.ProvinceItemResponse(**province.__dict__).dict(),
            }
            if province
            else None
        ),
        district=(
            {
                **schema_district.DistrictItemResponse(**district.__dict__).dict(),
            }
            if district
            else None
        ),
    )
    return work_location_response


def create_work_location_job(db: Session, job_id: int, data: dict):
    try:
        work_locations_data = [
            work_location_schema.WorkLocatioCreate(job_id=job_id, **work_location)
            for work_location in data
        ]

    except Exception as e:
        return custom_response_error(
            status_code=400,
            status=constant.ERROR,
            response=get_message_validation_error(e),
        )

    work_locations = []
    for work_location_data in work_locations_data:
        if not provinceCRUD.get(db, work_location_data.province_id):
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="Province not found"
            )
        if not districtCRUD.get(db, work_location_data.district_id):
            work_location = work_locationCRUD.create(
                db=db,
                obj_in={
                    "province_id": work_location_data.province_id,
                },
            )
            work_locations.append(work_location)
        work_location = work_locationCRUD.create(db=db, obj_in=work_location_data)
        work_locations.append(work_location)

    return work_locations


def create_work_location(db: Session, data: dict):
    try:
        work_location_data = work_location_schema.WorkLocatioCreate(**data)
    except Exception as e:
        return custom_response_error(
            status_code=400,
            status=constant.ERROR,
            response=get_message_validation_error(e),
        )

    if not provinceCRUD.get(db, work_location_data.province_id):
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Province not found"
        )
    if not districtCRUD.get(db, work_location_data.district_id):
        work_location = work_locationCRUD.create(
            db=db,
            obj_in={
                "province_id": work_location_data.province_id,
            },
        )
        return get_work_location_by_id(db, work_location.id)
    work_location = work_locationCRUD.create(db=db, obj_in=work_location_data)
    return get_work_location_by_work_location_id(db, work_location)


def update_work_location(db: Session, work_location_id: int, data: dict):
    work_location = work_locationCRUD.get(db, work_location_id)
    if not work_location:
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Working time not found"
        )

    try:
        work_location_data = work_location_schema.WorkLocatioUpdate(**data)
    except Exception as e:
        return custom_response_error(
            status_code=400,
            status=constant.ERROR,
            response=get_message_validation_error(e),
        )

    if work_location_data.province_id:
        if not provinceCRUD.get(db, work_location_data.province_id):
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="Province not found"
            )
    if work_location_data.district_id:
        if not districtCRUD.get(db, work_location_data.district_id):
            return custom_response_error(
                status_code=404, status=constant.ERROR, response="District not found"
            )

    work_location = work_locationCRUD.update(
        db=db, db_obj=work_location, obj_in=work_location_data
    )
    return get_work_location_by_work_location_id(db, work_location)


def update_work_location_job(
    db: Session, job_id: int, new_work_lcations: list, work_locations: list
):
    work_locations = []
    for work_location in work_locations:
        work_locationCRUD.remove(db, id=work_location.id)
    for work_location in new_work_lcations:
        work_location_in = work_location_schema.WorkLocatioCreate(
            job_id=job_id, **work_location
        )
        work_location = work_locationCRUD.create(db=db, obj_in=work_location_in)
        work_locations.append(work_location)
    return work_locations


def delete_work_location(db: Session, work_location_id: int):
    work_location = work_locationCRUD.get(db, work_location_id)
    if not work_location:
        return custom_response_error(
            status_code=404, status=constant.ERROR, response="Working time not found"
        )

    work_location = work_locationCRUD.remove(db, id=work_location_id)
    return work_location
