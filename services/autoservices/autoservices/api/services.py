from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from autoservices.database.database import get_db
from autoservices.models import models
from autoservices.schemas import schemas

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=schemas.ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    obj = models.Service(**service.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.Service).order_by(models.Service.id).all()
