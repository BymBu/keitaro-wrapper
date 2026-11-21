from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Keitaro Wrapper")


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}


@app.post("/api/campaigns", response_model=schemas.CampaignRead)
def create_campaign(payload: schemas.CampaignCreate, db: Session = Depends(get_db)):
    campaign = models.Campaign(
        name=payload.name,
        geo=payload.geo.upper(),
        offer_id=payload.offer_id,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@app.get("/api/campaigns", response_model=list[schemas.CampaignRead])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).order_by(models.Campaign.id.desc()).all()


@app.get("/api/campaigns/{campaign_id}", response_model=schemas.CampaignRead)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign