from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model.campaign import Campaign
from app.schema.campaign import CampaignCreate, CampaignUpdate
from app.hepler.enum import CampaignStatus, OrderType, SortBy


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
        if business_id:
            query = query.filter(self.model.business_id == business_id)
        if company_id:
            query = query.filter(self.model.company_id == company_id)
        if status:
            query = query.filter(self.model.status == status)
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

    def count(
        self,
        db: Session,
        *,
        business_id: int = None,
        company_id: int = None,
        status: CampaignStatus = None,
    ):
        query = db.query(self.model)
        if business_id:
            query = query.filter(self.model.business_id == business_id)
        if status:
            query = query.filter(self.model.status == status)
        if company_id:
            query = query.filter(self.model.company_id == company_id)
        return query.count()


campaign = CRUDCampaign(Campaign)
