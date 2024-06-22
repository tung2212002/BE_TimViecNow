from sqlalchemy.orm import Session
from typing import List
from redis import Redis

from app.crud.province import province as provinceCRUD
from app.crud.district import district as districtCRUD
from app.schema import (
    province as schema_province,
    district as schema_district,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


async def get_province(db: Session, redis: Redis, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    cache_key = f"provinces:{page.model_dump()}"
    provinces_response = None
    try:
        provinces_response = await redis.get_list(cache_key)
    except Exception as e:
        print(e)
        pass
    if not provinces_response:
        provinces_response = get_list_province_info(db, page.model_dump())
        try:
            expire_time = 60 * 60 * 24 * 7
            await redis.set_list(
                cache_key,
                [province.__dict__ for province in provinces_response],
                expire_time,
            )
        except Exception as e:
            print(e)
            pass
    return constant.SUCCESS, 200, provinces_response


async def get_district(db: Session, redis: Redis, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    province_id = data.get("province_id")
    if not province_id:
        return constant.ERROR, 400, "Province id is required"

    cache_key = f"districts:{province_id}:{page.model_dump()}"
    districts_response = None
    try:
        districts_response = await redis.get_list(cache_key)
    except Exception as e:
        print(e)
        pass
    if not districts_response:
        districts_response = get_list_district_info(
            db, {**page.model_dump(), "province_id": province_id}
        )
        try:
            expire_time = 60 * 60 * 24 * 7
            await redis.set_list(
                cache_key,
                [district.__dict__ for district in districts_response],
                expire_time,
            )
        except Exception as e:
            print(e)
            pass
    return constant.SUCCESS, 200, districts_response


async def get_province_by_id(db: Session, redis: Redis, id: int):
    province_response = None
    cache_key = f"provinces:{id}"
    try:
        await redis.set_dict(cache_key, province_response.__dict__)
    except Exception as e:
        pass

    if not province_response:
        province_response = get_province_info(db, id)
        if not province_response:
            return constant.ERROR, 404, "Province not found"
        dict_province = province_response.__dict__
        try:
            expire_time = 60 * 60 * 24 * 7
            await redis.set_dict(cache_key, dict_province, expire_time)
        except Exception as e:
            pass

    return constant.SUCCESS, 200, province_response


async def get_district_by_id(db: Session, redis: Redis, id: int):
    district_response = None
    cache_key = f"districts:{id}"
    try:
        district_response = await redis.get_dict(cache_key)
    except Exception as e:
        # log
        pass
    if not district_response:
        district_response = get_district_info(db, id)

        if not district_response:
            return constant.ERROR, 404, "District not found"
        try:
            expire_time = 60 * 60 * 24 * 7
            await redis.set_dict(cache_key, district_response.__dict__, expire_time)
        except Exception as e:
            # log
            pass

    return constant.SUCCESS, 200, district_response


async def get_district_by_id(db: Session, redis: Redis, id: int):
    district_response = None
    cache_key = f"districts:{id}"
    try:
        district_response = await redis.get_dict(cache_key)
    except Exception as e:
        pass
    if not district_response:
        district_response = get_district_info(db, id)
        if not district_response:
            return constant.ERROR, 404, "District not found"
        try:
            expire_time = 60 * 60 * 24 * 7
            await redis.set_dict(cache_key, district_response.__dict__, expire_time)
        except Exception as e:
            pass
    return constant.SUCCESS, 200, district_response


def get_province_info(db: Session, province_id: int):
    province = provinceCRUD.get(db, province_id)
    return (
        schema_province.ProvinceItemResponse(**province.__dict__) if province else None
    )


def get_district_info(db: Session, district_id: int):
    district = districtCRUD.get(db, district_id)
    return (
        schema_district.DistrictItemResponse(**district.__dict__) if district else None
    )


def get_list_district_info(db: Session, data: List[dict]):
    districts = districtCRUD.get_multi_by_province(db, **data)

    districts_response = [
        schema_district.DistrictItemResponse(**district.__dict__)
        for district in districts
    ]
    return districts_response


def get_list_province_info(db: Session, data: dict):
    provinces = provinceCRUD.get_multi(db, **data)

    provinces_response = [
        schema_province.ProvinceItemResponse(**province.__dict__)
        for province in provinces
    ]
    return provinces_response


def check_match_province_district(db: Session, province_id: int, district_id: int):
    district = districtCRUD.get(db, district_id)
    if not district or district.province_id != province_id:
        return custom_response_error(
            status=404, response="District id {} not found".format(district_id)
        )
    return True


def check_match_list_province_district(db: Session, data: List[dict]):
    for item in data:
        if not check_match_province_district(
            db, item.get("province_id"), item.get("district_id")
        ):
            return custom_response_error(
                status=404,
                response="District id {} not match with province id {}".format(
                    item.get("district_id"), item.get("province_id")
                ),
            )
    return True
