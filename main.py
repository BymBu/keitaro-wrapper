from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, get_db, Base
from app.keitaro_client import KeitaroClient

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Keitaro Wrapper")


@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}


@app.post("/api/campaigns", response_model=schemas.CampaignRead)
def create_campaign(payload: schemas.CampaignCreate, db: Session = Depends(get_db)):
    client = KeitaroClient()
    try:
        result = client.create_campaign_with_flows(
            name=payload.name,
            geo=payload.geo,
            offer_id=payload.offer_id,
        )
        campaign = models.Campaign(
            name=payload.name,
            geo=payload.geo.upper(),
            offer_id=payload.offer_id,
            keitaro_id=result["campaign"]["id"],
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        client.close()


@app.get("/api/campaigns", response_model=list[schemas.CampaignRead])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(models.Campaign).order_by(models.Campaign.id.desc()).all()


@app.get("/api/campaigns/{campaign_id}", response_model=schemas.CampaignRead)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


# --- Отладочные эндпоинты Keitaro ---

@app.get("/api/keitaro/offers")
def keitaro_offers():
    client = KeitaroClient()
    try:
        return client.list_offers()
    finally:
        client.close()


@app.get("/api/keitaro/groups")
def keitaro_groups():
    client = KeitaroClient()
    try:
        return client.list_groups()
    finally:
        client.close()


@app.get("/api/keitaro/domains")
def keitaro_domains():
    client = KeitaroClient()
    try:
        return client.list_domains()
    finally:
        client.close()