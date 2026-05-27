from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from warehouse.database.database import get_db
from warehouse.models import models
from warehouse.schemas import schemas

router = APIRouter(prefix="/parts", tags=["parts"])

@router.post("/", response_model=schemas.PartResponse, status_code=status.HTTP_201_CREATED)
def create_part(part: schemas.PartCreate, db: Session = Depends(get_db)):
    if db.query(models.Part).filter(models.Part.sku == part.sku).first():
        raise HTTPException(status_code=400, detail="Артикул уже существует")
    obj = models.Part(**part.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.PartResponse])
def list_parts(db: Session = Depends(get_db)):
    return db.query(models.Part).order_by(models.Part.id.desc()).all()

@router.patch("/{sku}/income", response_model=schemas.PartResponse)
def income_part(sku: str, operation: schemas.StockOperation, db: Session = Depends(get_db)):
    part = db.query(models.Part).filter(models.Part.sku == sku).first()
    if not part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    part.stock += operation.quantity
    db.commit()
    db.refresh(part)
    return part

@router.patch("/{sku}/writeoff", response_model=schemas.PartResponse)
def writeoff_part(sku: str, operation: schemas.StockOperation, db: Session = Depends(get_db)):
    part = db.query(models.Part).filter(models.Part.sku == sku).first()
    if not part:
        raise HTTPException(status_code=404, detail="Запчасть не найдена")
    if part.stock < operation.quantity:
        raise HTTPException(status_code=400, detail="Недостаточно товара на складе")
    part.stock -= operation.quantity
    db.commit()
    db.refresh(part)
    return part
