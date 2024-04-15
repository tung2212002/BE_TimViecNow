from sqlalchemy.orm import Session

from app.crud.province import province as provinceCRUD
from app.crud.district import district as districtCRUD
from app.schema import (
    province as schema_province,
    district as schema_district,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error


def get_list_province(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    provinces = provinceCRUD.get_multi(db, **page.dict())

    provinces_response = [
        schema_province.ProvinceItemResponse(**province.__dict__)
        for province in provinces
    ]
    return constant.SUCCESS, 200, provinces_response


def get_list_district(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    province_id = data.get("province_id")
    if not province_id:
        return constant.ERROR, 400, "Province id is required"

    districts = districtCRUD.get_multi_by_province(
        db, **{**page.dict(), "province_id": province_id}
    )
    districts_response = [
        schema_district.DistrictItemResponse(**district.__dict__)
        for district in districts
    ]
    return constant.SUCCESS, 200, districts_response


def get_province_by_id(db: Session, province_id: int):
    province = provinceCRUD.get(db, province_id)
    if not province:
        return constant.ERROR, 404, "Province not found"
    province_response = schema_province.ProvinceItemResponse(**province.__dict__)
    return constant.SUCCESS, 200, province_response


def get_district_by_id(db: Session, district_id: int):
    district = districtCRUD.get(db, district_id)
    if not district:
        return constant.ERROR, 404, "District not found"
    district_response = schema_district.DistrictItemResponse(**district.__dict__)
    return constant.SUCCESS, 200, district_response
