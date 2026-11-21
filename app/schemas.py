from datetime import datetime
from pydantic import BaseModel, Field


class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    geo: str = Field(..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2, например RU, US")
    offer_id: int = Field(..., gt=0)


class CampaignRead(BaseModel):
    id: int
    name: str
    geo: str
    offer_id: int
    keitaro_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}