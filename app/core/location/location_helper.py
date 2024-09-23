from sqlalchemy.orm import Session

from app import crud
from app.schema import (
    province as schema_province,
    district as schema_district,
)
from app.common.exception import CustomException
from fastapi import status


class LocationHelper:
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

    def get_list_district_info(self, db: Session, data: dict) -> list:
        districts = crud.district.get_multi_by_province(db, **data)
        return [
            schema_district.DistrictItemResponse(**district.__dict__)
            for district in districts
        ]

    def check_valid_province_district(
        self, db: Session, province_id: int, district_id: int
    ) -> None:
        province = self.get_province_info_by_id(db, province_id)
        if not province:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Province not found"
            )

        if district_id:
            district = self.get_district_info_by_id(db, district_id)
            if not district:
                raise CustomException(
                    status_code=status.HTTP_400_BAD_REQUEST, msg="District not found"
                )


location_helper = LocationHelper()
