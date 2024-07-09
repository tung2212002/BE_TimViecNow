from sqlalchemy.orm import Session
from datetime import date, timedelta
from sqlalchemy.sql import func, text

from .base import CRUDBase
from app.model import Job, Campaign, CVApplication
from app.schema.campaign import CampaignCreate, CampaignUpdate
from app.hepler.enum import (
    CampaignStatus,
    OrderType,
    SortBy,
    JobStatus,
    CVApplicationStatus,
)


class CRUDCampaign(CRUDBase[Campaign, CampaignCreate, CampaignUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        skip=0,
        limit=10,
        sort_by: SortBy = SortBy.ID,
        order_by: OrderType = OrderType.DESC,
        status: CampaignStatus = None,
    ):
        query = db.query(self.model)
        query = self.apply_filter(
            query, business_id=business_id, company_id=company_id, status=status
        )
        return self.return_campaign(query, skip, limit, sort_by, order_by)

    def count(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        status: CampaignStatus = None,
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(
            query, business_id=business_id, company_id=company_id, status=status
        )
        return query.scalar()

    def get_has_published_job(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        skip=0,
        limit=10,
        sort_by: SortBy = SortBy.ID,
        order_by: OrderType = OrderType.DESC,
    ):
        query = db.query(self.model)
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
            job_deadline=True,
        )
        return self.return_campaign(query, skip, limit, sort_by, order_by)

    def count_has_published_job(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
            job_status=JobStatus.PUBLISHED,
            job_deadline=True,
        )
        return query.scalar()

    def get_open(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        skip=0,
        limit=10,
        sort_by: SortBy = SortBy.ID,
        order_by: OrderType = OrderType.DESC,
    ):
        query = db.query(self.model)
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
        )
        return self.return_campaign(query, skip, limit, sort_by, order_by)

    def count_open(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
        )
        return query.scalar()

    def get_has_new_application(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        skip=0,
        limit=10,
        sort_by: SortBy = SortBy.ID,
        order_by: OrderType = OrderType.DESC,
    ):
        query = db.query(self.model)
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            job_status=JobStatus.PUBLISHED,
            Job_deadline=True,
        )
        query = query.join(CVApplication).filter(
            CVApplication.status == CVApplicationStatus.PENDING
            and CVApplication.created_at >= func.now() - text("INTERVAL 1 DAY")
        )
        return self.return_campaign(query, skip, limit, sort_by, order_by)

    def count_has_new_application(
        self, db: Session, *, business_id: int = None, Company_id: int = None
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(query, business_id=business_id, company_id=Company_id)
        query = query.join(Job).filter(
            Job.status == JobStatus.PUBLISHED, Job.deadline >= func.now()
        )
        query = query.join(CVApplication).filter(
            CVApplication.status == CVApplicationStatus.PENDING
            and CVApplication.created_at >= func.now() == date.timedelta(days=1)
        )
        return query.scalar()

    def get_has_published(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
        )
        query = query.join(Job).filter(Job.status == JobStatus.PUBLISHED)
        return query.scalar()

    def count_has_published(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
            job_status=JobStatus.PUBLISHED,
        )
        return query.scalar()

    def get_has_published_job_expired(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        skip=0,
        limit=10,
        sort_by: SortBy = SortBy.ID,
        order_by: OrderType = OrderType.DESC,
    ):
        query = db.query(self.model)
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
        )
        query = query.join(Job).filter(
            Job.status == JobStatus.PUBLISHED, Job.deadline < func.now()
        )
        return self.return_campaign(query, skip, limit, sort_by, order_by)

    def count_has_published_job_expired(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
        )
        query = query.join(Job).filter(
            Job.status == JobStatus.PUBLISHED, Job.deadline < func.now()
        )
        return query.scalar()

    def get_has_pending_job(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        skip=0,
        limit=10,
        sort_by: SortBy = SortBy.ID,
        order_by: OrderType = OrderType.DESC,
    ):
        query = db.query(self.model)
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
            job_status=JobStatus.PENDING,
        )
        return self.return_campaign(query, skip, limit, sort_by, order_by)

    def count_has_pending_job(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
    ):
        query = db.query(func.count(self.model.id))
        query = self.apply_filter(
            query,
            business_id=business_id,
            company_id=company_id,
            status=CampaignStatus.OPEN,
            job_status=JobStatus.PENDING,
        )
        return query.scalar()

    def apply_filter(
        self,
        query,
        *,
        business_id: int = None,
        company_id: int = None,
        status: CampaignStatus = None,
        job_status: JobStatus = None,
        job_deadline: bool = False,
    ):
        if business_id:
            query = query.filter(self.model.business_id == business_id)
        if status:
            query = query.filter(self.model.status == status)
        if company_id:
            query = query.filter(self.model.company_id == company_id)
        if job_status or job_deadline:
            query = query.join(Job)
            if job_deadline:
                query = query.filter(Job.deadline >= func.now())
            if job_status:
                query = query.filter(Job.status == job_status)

        return query

    def return_campaign(self, query, skip, limit, sort_by, order_by):
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


campaign = CRUDCampaign(Campaign)
