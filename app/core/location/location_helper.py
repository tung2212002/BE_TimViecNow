from sqlalchemy.orm import Session
from typing import List

from app.model import Province, District
from app.crud import province as provinceCRUD, district as districtCRUD
from app.schema.province import ProvinceItemResponse
from app.schema.district import DistrictItemResponse
from app.common.exception import CustomException
from fastapi import status


class LocationHelper:
    def get_province_info_by_id(self, db: Session, id: int) -> ProvinceItemResponse:
        province = provinceCRUD.get(db, id)
        return ProvinceItemResponse(**province.__dict__) if province else None

    def get_province_info(self, province: Province) -> ProvinceItemResponse:
        return ProvinceItemResponse(**province.__dict__) if province else None

    def get_district_info_by_id(self, db: Session, id: int) -> DistrictItemResponse:
        district = districtCRUD.get(db, id)
        return DistrictItemResponse(**district.__dict__) if district else None

    def get_district_info(self, district: District) -> DistrictItemResponse:
        return DistrictItemResponse(**district.__dict__) if district else None

    def get_list_province_info(
        self, db: Session, data: dict
    ) -> List[ProvinceItemResponse]:
        provinces = provinceCRUD.get_multi(db, **data)
        return [ProvinceItemResponse(**province.__dict__) for province in provinces]

    def get_list_district_info(
        self, db: Session, data: dict
    ) -> List[DistrictItemResponse]:
        districts = districtCRUD.get_multi_by_province(db, **data)
        return [DistrictItemResponse(**district.__dict__) for district in districts]

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
