from sqlalchemy.orm import Session
from redis.asyncio import Redis

from app import crud
from app.schema import (
    skill as schema_skill,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.storage.cache.config_cache_service import config_cache_service
from app.core.skill.skill_helper import skill_helper


# async def get(db: Session, redis: Redis, data: dict):
#     page = skill_helper.validate_pagination(data)
#     try:
#         skills_response = await config_cache_service.get_cache_skill(redis)
#     except Exception as e:
#         print(e)
#     if not skills_response:
#         skills_response = skill_helper.get_list_info(db, page.model_dump())
#         try:
#             await config_cache_service.cache_skill(
#                 redis, [skill.__dict__ for skill in skills_response]
#             )
#         except Exception as e:
#             print(e)
#     return constant.SUCCESS, 200, skills_response


# async def get_by_id(db: Session, id: int):
#     skill_response = skill_helper.get_info_by_id(db, id)
#     if not skill_response:
#         return constant.ERROR, 404, "Skill not found"
#     return constant.SUCCESS, 200, skill_response


# async def update(db: Session, id: int, data: dict):
#     skill = crud.skill.get(db, id)
#     if not skill:
#         return constant.ERROR, 404, "Skill not found"

#     skill_data = schema_skill.SkillUpdateRequest(**data)

#     skill = crud.skill.update(db, db_obj=skill, obj_in=skill_data)
#     return constant.SUCCESS, 200, skill


# async def delete(db: Session, id: int):
#     skill = crud.skill.get(db, id)
#     if not skill:
#         return constant.ERROR, 404, "Skill not found"

#     skill = crud.skill.remove(db, id=id)
#     return constant.SUCCESS, 200, skill


class SkillService:
    async def get(self, db: Session, redis: Redis, data: dict):
        page = skill_helper.validate_pagination(data)
        try:
            skills_response = await config_cache_service.get_cache_skill(redis)
        except Exception as e:
            print(e)
        if not skills_response:
            skills = crud.skill.get_multi(db, **page.model_dump())
            skills_response = skill_helper.get_list_info(skills)
            try:
                await config_cache_service.cache_skill(
                    redis, [skill.__dict__ for skill in skills_response]
                )
            except Exception as e:
                print(e)
        return constant.SUCCESS, 200, skills_response

    async def get_by_id(self, db: Session, id: int):
        skill_response = skill_helper.get_info_by_id(db, id)
        if not skill_response:
            return constant.ERROR, 404, "Skill not found"
        return constant.SUCCESS, 200, skill_response

    async def update(self, db: Session, id: int, data: dict):
        skill = crud.skill.get(db, id)
        if not skill:
            return constant.ERROR, 404, "Skill not found"

        skill_data = schema_skill.SkillUpdateRequest(**data)

        skill = crud.skill.update(db, db_obj=skill, obj_in=skill_data)
        return constant.SUCCESS, 200, skill

    async def delete(self, db: Session, id: int):
        skill = crud.skill.get(db, id)
        if not skill:
            return constant.ERROR, 404, "Skill not found"

        skill = crud.skill.remove(db, id=id)
        return constant.SUCCESS, 200, skill


skill_service = SkillService()

# def get_skill_info(db: Session, skill):
#     return schema_skill.SkillItemResponse(**skill.__dict__) if skill else None


# def get_list_skill_by_model(db: Session, skills):
#     return [schema_skill.SkillItemResponse(**skill.__dict__) for skill in skills]


# def get_skill_info_by_id(db: Session, skill_id: int):
#     skill = crud.skill.get(db, skill_id)
#     return schema_skill.SkillItemResponse(**skill.__dict__) if skill else None


# def get_list_skill_info(db: Session, data: dict):
#     skills = crud.skill.get_multi(db, **data)
#     return [
#         schema_skill.SkillItemResponse(**skill.__dict__) if skill else None
#         for skill in skills
#     ]


# def get_list_skill_by_ids(db: Session, skill_ids: list):
#     skills_response = [get_skill_info_by_id(db, skill_id) for skill_id in skill_ids]
#     return skills_response


# def check_skill_exist(db: Session, skill_id: int):
#     skill = crud.skill.get(db, skill_id)
#     if not skill:
#         return custom_response_error(
#             status=404, response="Skill id {} not found".format(skill_id)
#         )
#     return skill


# def check_skills_exist(db: Session, skill_ids: list):
#     if not skill_ids:
#         return []
#     list_skills = []
#     for skill_id in skill_ids:
#         skill = check_skill_exist(db, skill_id)
#         list_skills.append(skill)
#     return list_skills


# def create_skill(db: Session, data: dict):
#     try:
#         skill_data = schema_skill.SkillCreateRequest(**data)
#     except Exception as e:
#         return constant.ERROR, 400, get_message_validation_error(e)
#     skill = crud.skill.get_by_name(db, skill_data.name)
#     if skill:
#         return constant.ERROR, 409, "Skill already registered"

#     skill = crud.skill.create(db, obj_in=skill_data)
#     return constant.SUCCESS, 201, skill


# def create_skill_job(db: Session, job_id: int, skill_ids: list):
#     skill_ids = list(set(skill_ids))
#     for skill_id in skill_ids:
#         crud.job_skill.create(db, obj_in={"job_id": job_id, "skill_id": skill_id})
#     return skill_ids


# def update_skill_job(db: Session, job_id: int, new_skill_ids: list):
#     new_skill_ids = list(set(new_skill_ids))
#     current_skill = crud.job_skill.get_by_job_id(db, job_id)
#     current_skill_ids = [skill.id for skill in current_skill]
#     add_skill_ids = list(set(new_skill_ids) - set(current_skill_ids))
#     full_skill_ids = list(set(new_skill_ids) | set(current_skill_ids))

#     for skill_id in full_skill_ids:
#         if skill_id in add_skill_ids:
#             crud.job_skill.create(db, obj_in={"job_id": job_id, "skill_id": skill_id})
#         elif
