from sqlalchemy.orm import Session
from fastapi import status
from redis.asyncio import Redis

from app.crud import skill as skillCRUD
from app.schema.skill import SkillCreateRequest, SkillUpdateRequest
from app.schema.page import Pagination
from app.core import constant
from app.storage.cache.config_cache_service import config_cache_service
from app.core.skill.skill_helper import skill_helper
from app.common.exception import CustomException
from app.common.response import CustomResponse


class SkillService:
    async def get(self, db: Session, redis: Redis, data: dict):
        page = Pagination(**data)
        key = page.get_key()

        response = None
        try:
            response = await config_cache_service.get_cache_skill(redis, key)
        except Exception as e:
            print(e)
        if not response:
            skills = skillCRUD.get_multi(db, **page.model_dump())
            response = skill_helper.get_list_info(skills)
            try:
                await config_cache_service.cache_skill(redis, key, response)
            except Exception as e:
                print(e)

        return CustomResponse(data=response)

    async def get_by_id(self, db: Session, id: int):
        response = skill_helper.get_info_by_id(db, id)
        if not response:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Skill not found"
            )

        return CustomResponse(data=response)

    async def create(self, db: Session, data: dict):
        skill_data = SkillCreateRequest(**data)
        response = skillCRUD.create(db, obj_in=skill_data)

        return CustomResponse(data=response)

    async def update(self, db: Session, id: int, data: dict):
        skill = skillCRUD.get(db, id)
        if not skill:
            return constant.ERROR, 404, "Skill not found"

        skill_data = SkillUpdateRequest(**data)

        response = skillCRUD.update(db, db_obj=skill, obj_in=skill_data)

        return CustomResponse(data=response)

    async def delete(self, db: Session, id: int):
        skill = skillCRUD.get(db, id)
        if not skill:
            return constant.ERROR, 404, "Skill not found"

        skillCRUD.remove(db, id=id)

        return CustomResponse(msg="Skill has been deleted")


skill_service = SkillService()
