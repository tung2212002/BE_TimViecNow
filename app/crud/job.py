from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model.job import Job
from app.schema.job import JobCreate, JobUpdate


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    def get_multi(
        self,
        db: Session,
        business_id: int = None,
        company_id=None,
        *,
        skip=0,
        limit=10,
        sort_by="id",
        order_by="asc"
    ):
        query = db.query(self.model)
        if business_id:
            query = query.filter(self.model.business_id == business_id)
        if company_id:
            query = query.filter(self.model.company_id == company_id)
        return (
            query.order_by(
                getattr(self.model, sort_by).desc()
                if order_by == "desc"
                else getattr(self.model, sort_by)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


job = CRUDJob(Job)
