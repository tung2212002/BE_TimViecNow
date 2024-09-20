from sqlalchemy.orm import Session
from redis.asyncio import Redis
from typing import List, Optional

from app import crud
from app.schema import (
    skill as schema_skill,
    job_skill as schema_job_skill,
    page as schema_page,
)
from app.core import constant
from app.hepler.exception_handler import get_message_validation_error
from app.hepler.response_custom import custom_response_error
from app.core.helper_base import HelperBase
from app.model import Skill
from app.hepler.enum import JobSkillType


class SkillHelper(HelperBase):

    def get_info(self, skill: Skill) -> dict:
        return schema_skill.SkillItemResponse(**skill.__dict__)

    def get_list_info(self, skills: List[Skill]) -> list:
        return [self.get_info(skill) for skill in skills]

    def get_info_by_id(self, db: Session, id: int) -> dict:
        skill = crud.skill.get(db, id)
        return self.get_info(db, skill) if skill else None

    def get_list_by_ids(self, db: Session, ids: list[int]) -> list:
        return [self.get_info_by_id(db, id) for id in ids]

    def check_valid(self, db: Session, id: int) -> int:
        skill = crud.skill.get(db, id)
        if not skill:
            return custom_response_error(
                status_code=404,
                status=constant.ERROR,
                response=f"Skill with id {id} not found",
            )

        return id

    def check_list_valid(self, db: Session, ids: list[int]) -> bool:
        return [self.check_valid(db, id) for id in ids]

    def create_with_job_id(
        self,
        db: Session,
        job_id: int,
        ids: list[dict],
        type: JobSkillType = JobSkillType.MUST_HAVE,
    ) -> list:
        ids = list(set(ids))
        for skill in ids:
            skill = crud.skill.create(
                db,
                schema_job_skill.JobSkillCreate(
                    job_id=job_id, skill_id=skill, type=type
                ),
            )

        return ids

    def update_with_job_id(
        self,
        db: Session,
        job_id: int,
        new_skill_ids: list[dict],
        type: JobSkillType = JobSkillType.MUST_HAVE,
    ) -> list:
        ids = set(new_skill_ids)
        current_skill_ids = crud.job_skill.get_ids_by_job_id(db, job_id)
        add_skill_ids = list(ids - set(current_skill_ids))
        remove_skill_ids = list(set(current_skill_ids) - ids)

        for skill_id in add_skill_ids:
            crud.job_skill.create(
                db, schema_job_skill.JobSkillCreate(job_id=job_id, skill_id=skill_id)
            )
        for skill_id in remove_skill_ids:
            crud.job_skill.remove_by_job_id_and_skill_id(db, job_id, skill_id)
        return new_skill_ids


skill_helper = SkillHelper(
    schema_page.Pagination,
    schema_skill.SkillCreateRequest,
    schema_skill.SkillUpdateRequest,
)