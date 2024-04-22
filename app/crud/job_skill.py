from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import JobSkill
from app.schema.job_skill import JobSkillCreate, JobSkillUpdate


class CRUDJobSkill(CRUDBase[JobSkill, JobSkillCreate, JobSkillUpdate]):
    def get_by_job_id_and_skill_id(
        self, db: Session, job_id: int, skill_id: int
    ) -> JobSkill:
        return (
            db.query(self.model)
            .filter(self.model.job_id == job_id)
            .filter(self.model.skill_id == skill_id)
            .first()
        )

    def remove_by_job_id_and_skill_id(
        self, db: Session, job_id: int, skill_id: int
    ) -> None:
        db.query(self.model).filter(self.model.job_id == job_id).filter(
            self.model.skill_id == skill_id
        ).delete()
        db.commit()


job_skill = CRUDJobSkill(JobSkill)
