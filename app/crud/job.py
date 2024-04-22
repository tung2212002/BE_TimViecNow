from typing import Type
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model.job import Job
from app.model.job_approval_request import JobApprovalRequest
from app.model.business import Business
from app.schema.job import JobCreate, JobUpdate
from app.hepler.enum import JobStatus, JobApprovalStatus


class CRUDJob(CRUDBase[Job, JobCreate, JobUpdate]):
    def __init__(self, model: Type[Job]):
        super().__init__(model)
        self.job_approval_request = JobApprovalRequest
        self.business = Business

    def get_multi(
        self,
        db: Session,
        business_id: int = None,
        company_id: int = None,
        campaign_id: int = None,
        *,
        skip=0,
        limit=10,
        sort_by="id",
        order_by="asc",
        job_status=JobStatus.ALL,
        job_approve_status=JobApprovalStatus.ALL,
    ):
        query = db.query(self.model)
        if campaign_id:
            query = query.filter(self.model.campaign_id == campaign_id)
        if business_id:
            query = query.filter(self.model.business_id == business_id)
        if job_status != JobStatus.ALL:
            query = query.filter(self.model.status == job_status)
        if job_approve_status != JobApprovalStatus.ALL:
            query = query.join(
                self.job_approval_request,
                self.model.id == self.job_approval_request.job_id,
            ).filter(self.job_approval_request.status == job_approve_status)
        if company_id:
            query = query.join(
                self.business, self.model.business_id == self.business.id
            ).filter(self.business.company_id == company_id)
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

    def get_by_campaign_id(self, db: Session, campaign_id: int):
        return (
            db.query(self.model).filter(self.model.campaign_id == campaign_id).first()
        )


job = CRUDJob(Job)
