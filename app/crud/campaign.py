from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model.campaign import Campaign
from app.schema.campaign import CampaignCreateRequest, CampaignUpdateRequest


class CRUDCampaign(CRUDBase[Campaign, CampaignCreateRequest, CampaignUpdateRequest]):
    def get_multi(
        self,
        db: Session,
        business_id: int = None,
        status: int = None,
        *,
        skip=0,
        limit=10,
        sort_by="id",
        order_by="asc"
    ):
        query = db.query(self.model)
        if business_id:
            query = query.filter(self.model.business_id == business_id)
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


campaign = CRUDCampaign(Campaign)
