from sqlalchemy.orm import Session

from .base import CRUDBase
from app.model.campaign import Campaign
from app.schema.campaign import CampaignCreateRequest, CampaignUpdateRequest


class CRUDCampaign(CRUDBase[Campaign, CampaignCreateRequest, CampaignUpdateRequest]):
    pass


campaign = CRUDCampaign(Campaign)
