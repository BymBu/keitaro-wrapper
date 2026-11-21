from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    geo = Column(String, nullable=False)
    offer_id = Column(Integer, nullable=False)
    keitaro_id = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())