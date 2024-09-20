from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.schema import (
    province as schema_province,
    district as schema_district,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


class LocationHelper:
    def validate_pagination(
        self,
        data: dict,
    ):
        try:
            page = schema_page.Pagination(**data)
        except Exception as e:
            return custom_response_error(
                status_code=400,
                status=constant.ERROR,
                response=get_message_validation_error(e),
            )
        return page

    def get_province_info_by_id(self, db: Session, id: int) -> dict:
        province = crud.province.get(db, id)
        return (
            schema_province.ProvinceItemResponse(**province.__dict__)
            if province
            else None
        )

    def get_district_info_by_id(self, db: Session, id: int) -> dict:
        district = crud.district.get(db, id)
        return (
            schema_district.DistrictItemResponse(**district.__dict__)
            if district
            else None
        )

    def get_list_province_info(self, db: Session, data: dict) -> list:
        provinces = crud.province.get_multi(db, **data)
        return [
            schema_province.ProvinceItemResponse(**province.__dict__)
            for province in provinces
        ]


location_helper = LocationHelper()
