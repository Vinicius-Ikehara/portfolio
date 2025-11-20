from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/profile",
    tags=["profile"]
)


@router.get("/", response_model=schemas.Profile)
def get_profile(db: Session = Depends(get_db)):
    profile = db.query(models.Profile).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    # Verifica se já existe um perfil
    existing_profile = db.query(models.Profile).first()
    if existing_profile:
        raise HTTPException(status_code=400, detail="Profile already exists. Use PUT to update.")

    db_profile = models.Profile(**profile.model_dump())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.put("/", response_model=schemas.Profile)
def update_profile(profile: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    db_profile = db.query(models.Profile).first()
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    update_data = profile.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile
