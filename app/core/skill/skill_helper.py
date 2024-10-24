from sqlalchemy.orm import Session
from typing import List

from app.crud import skill as skillCRUD, job_skill as job_skillCRUD
from app.schema.skill import SkillItemResponse
from app.schema.job_skill import JobSkillCreate
from app.model import Skill
from app.hepler.enum import JobSkillType
from app.common.exception import CustomException
from fastapi import status


class SkillHelper:
    def get_info(self, skill: Skill) -> dict:
        return SkillItemResponse(**skill.__dict__)

    def get_list_info(self, skills: List[Skill]) -> list:
        return [self.get_info(skill) for skill in skills]

    def get_info_by_id(self, db: Session, id: int) -> dict:
        skill = skillCRUD.get(db, id)
        return self.get_info(db, skill) if skill else None

    def get_list_by_ids(self, db: Session, ids: list[int]) -> list:
        return [self.get_info_by_id(db, id) for id in ids]

    def check_valid(self, db: Session, id: int) -> int:
        skill = skillCRUD.get(db, id)
        if not skill:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND, msg="Skill not found"
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
            skill = job_skillCRUD.create(
                db,
                obj_in=JobSkillCreate(job_id=job_id, skill_id=skill, type=type),
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
        current_skill_ids = job_skillCRUD.get_ids_by_job_id(db, job_id)
        add_skill_ids = list(ids - set(current_skill_ids))
        remove_skill_ids = list(set(current_skill_ids) - ids)

        for skill_id in add_skill_ids:
            job_skillCRUD.create(db, JobSkillCreate(job_id=job_id, skill_id=skill_id))
        for skill_id in remove_skill_ids:
            job_skillCRUD.remove_by_job_id_and_skill_id(db, job_id, skill_id)
        return new_skill_ids


skill_helper = SkillHelper()
