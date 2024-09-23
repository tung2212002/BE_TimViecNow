from sqlalchemy.orm import Session
from typing import List

from .base import CRUDBase
from app.model import WorkLocation
from app.schema.work_location import WorkLocatioCreate, WorkLocatioUpdate


class CRUDWorkLocation(CRUDBase[WorkLocation, WorkLocatioCreate, WorkLocatioUpdate]):
    def get_by_job_id(self, db: Session, job_id: int) -> List[WorkLocation]:
        work_locations = db.query(self.model).filter(self.model.job_id == job_id).all()
        return work_locations

    def remove_by_job_id(self, db: Session, job_id: int) -> None:
        db.query(self.model).filter(self.model.job_id == job_id).delete()
        db.commit()


work_location = CRUDWorkLocation(WorkLocation)
