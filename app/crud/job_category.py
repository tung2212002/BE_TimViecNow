from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model import JobCategory
from app.schema.job_category import JobCategoryCreate, JobCategoryUpdate


class CRUDJobCategory(CRUDBase[JobCategory, JobCategoryCreate, JobCategoryUpdate]):
    def get_by_job_id_and_category_id(
        self, db: Session, job_id: int, category_id: int
    ) -> JobCategory:
        return (
            db.query(self.model)
            .filter(self.model.job_id == job_id)
            .filter(self.model.category_id == category_id)
            .first()
        )

    def remove_by_job_id_and_category_id(
        self, db: Session, job_id: int, category_id: int
    ) -> None:
        db.query(self.model).filter(self.model.job_id == job_id).filter(
            self.model.category_id == category_id
        ).delete()
        db.commit()


job_category = CRUDJobCategory(JobCategory)
