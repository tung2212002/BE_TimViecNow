from sqlalchemy.orm import Session


from .base import CRUDBase
from app.model import WorkingTime
from app.schema.working_time import WorkingTimeCreate, WorkingTimeUpdate


class CRUDWorkingTime(CRUDBase[WorkingTime, WorkingTimeCreate, WorkingTimeUpdate]):
    def get_working_times_by_job_id(self, db: Session, job_id: int):
        working_times = db.query(self.model).filter(self.model.job_id == job_id).all()
        return working_times


working_time = CRUDWorkingTime(WorkingTime)
