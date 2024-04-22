from sqlalchemy.orm import Session

from app.crud.skill import skill as skillCRUD
from app.crud.job_skill import job_skill as job_skillCRUD
from app.schema import (
    skill as schema_skill,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error


def get_list_skill(db: Session, data: dict):
    try:
        page = schema_page.Pagination(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    skills = skillCRUD.get_multi(db, **page.dict())

    skills_response = get_list_skill(db, skills)
    return constant.SUCCESS, 200, skills_response


def get_skill_by_id(db: Session, skill_id: int):
    skill_response = get_skill_info_by_id(db, skill_id)
    if not skill_response:
        return constant.ERROR, 404, "Skill not found"
    return constant.SUCCESS, 200, skill_response


def get_skill_info(db: Session, skill):
    return schema_skill.SkillItemResponse(**skill.__dict__) if skill else None


def get_list_skill_by_model(db: Session, skills):
    return [schema_skill.SkillItemResponse(**skill.__dict__) for skill in skills]


def get_skill_info_by_id(db: Session, skill_id: int):
    skill = skillCRUD.get(db, skill_id)
    return schema_skill.SkillItemResponse(**skill.__dict__) if skill else None


def get_list_skill_info(db: Session, data: dict):
    skills = skillCRUD.get_multi(db, **data)
    return [
        schema_skill.SkillItemResponse(**skill.__dict__) if skill else None
        for skill in skills
    ]


def get_list_skill_by_ids(db: Session, skill_ids: list):
    skills_response = [get_skill_info_by_id(db, skill_id) for skill_id in skill_ids]
    return skills_response


def check_skill_exist(db: Session, skill_id: int):
    skill = skillCRUD.get(db, skill_id)
    if not skill:
        return custom_response_error(
            status=404, response="Skill id {} not found".format(skill_id)
        )
    return skill


def check_skills_exist(db: Session, skill_ids: list):
    list_skills = []
    for skill_id in skill_ids:
        skill = check_skill_exist(db, skill_id)
        list_skills.append(skill)
    return list_skills


def create_skill(db: Session, data: dict):
    try:
        skill_data = schema_skill.SkillCreateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)
    skill = skillCRUD.get_by_name(db, skill_data.name)
    if skill:
        return constant.ERROR, 409, "Skill already registered"

    skill = skillCRUD.create(db, obj_in=skill_data)
    return constant.SUCCESS, 201, skill


def create_skill_job(db: Session, job_id: int, skill_ids: list):
    skill_ids = list(set(skill_ids))
    for skill_id in skill_ids:
        job_skillCRUD.create(db, obj_in={"job_id": job_id, "skill_id": skill_id})
    return skill_ids


def update_skill(db: Session, skill_id: int, data: dict):
    skill = skillCRUD.get(db, skill_id)
    if not skill:
        return constant.ERROR, 404, "Skill not found"

    try:
        skill_data = schema_skill.SkillUpdateRequest(**data)
    except Exception as e:
        return constant.ERROR, 400, get_message_validation_error(e)

    skill = skillCRUD.update(db, db_obj=skill, obj_in=skill_data)
    return constant.SUCCESS, 200, skill


def update_skill_job(db: Session, new_skill_ids: list, skills: list):
    new_skill_ids = list(set(new_skill_ids))
    current_skill_ids = [skill.skill_id for skill in skills]
    add_skill_ids = list(set(new_skill_ids) - set(current_skill_ids))
    for skill in skills:
        if skill.skill_id not in new_skill_ids:
            job_skillCRUD.remove(db, id=skill.id)
    for skill_id in add_skill_ids:
        job_skillCRUD.create(db, obj_in={"job_id": skill.job_id, "skill_id": skill_id})
    return new_skill_ids


def delete_skill(db: Session, skill_id: int):
    skill = skillCRUD.get(db, skill_id)
    if not skill:
        return constant.ERROR, 404, "Skill not found"

    skill = skillCRUD.remove(db, id=skill_id)
    return constant.SUCCESS, 200, skill
