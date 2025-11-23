from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db
from ..dependencies import verify_admin_token

router = APIRouter(
    prefix="/api/experiences",
    tags=["experiences"]
)


@router.get("/", response_model=List[schemas.Experience])
def get_experiences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiences = db.query(models.Experience).order_by(models.Experience.order).offset(skip).limit(limit).all()
    return experiences


@router.get("/{experience_id}", response_model=schemas.Experience)
def get_experience(experience_id: int, db: Session = Depends(get_db)):
    experience = db.query(models.Experience).filter(models.Experience.id == experience_id).first()
    if experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience


@router.post("/", response_model=schemas.Experience)
def create_experience(
    experience: schemas.ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_admin_token)
):
    db_experience = models.Experience(**experience.model_dump())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.put("/{experience_id}", response_model=schemas.Experience)
def update_experience(
    experience_id: int,
    experience: schemas.ExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_admin_token)
):
    db_experience = db.query(models.Experience).filter(models.Experience.id == experience_id).first()
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    update_data = experience.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_experience, key, value)

    db.commit()
    db.refresh(db_experience)
    return db_experience


@router.delete("/{experience_id}")
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_admin_token)
):
    db_experience = db.query(models.Experience).filter(models.Experience.id == experience_id).first()
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    db.delete(db_experience)
    db.commit()
    return {"message": "Experience deleted successfully"}
