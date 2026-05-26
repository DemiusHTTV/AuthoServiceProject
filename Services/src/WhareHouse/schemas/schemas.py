from pydantic import BaseModel, Field

class PartCreate(BaseModel):
    name: str

class PartResponse(BaseModel):
    id: int
    name: str
    class Config: from_attributes = True

class WarehouseUpdate(BaseModel):
    part_id: int
    quantity: int = Field(..., ge=0)

class WarehouseResponse(BaseModel):
    id: int
    part_id: int
    quantity: int
    class Config: from_attributes = True