from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from autoservices.database.database import get_db
from autoservices.models import models
from autoservices.schemas import schemas

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    obj = models.Employee(**employee.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.get("/", response_model=list[schemas.EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).order_by(models.Employee.id).all()
