from sqlalchemy.orm import Session
from typing import List

from .base import CRUDBase
from app.model import WorkingTime
from app.schema.working_time import WorkingTimeCreate, WorkingTimeUpdate


class CRUDWorkingTime(CRUDBase[WorkingTime, WorkingTimeCreate, WorkingTimeUpdate]):
    def get_by_job_id(self, db: Session, job_id: int) -> List[WorkingTime]:
        return db.query(self.model).filter(self.model.job_id == job_id).all()

    def remove_by_job_id(self, db: Session, job_id: int) -> bool:
        db.query(self.model).filter(self.model.job_id == job_id).delete()
        db.commit()
        return True


working_time = CRUDWorkingTime(WorkingTime)
