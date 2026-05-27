from pydantic import BaseModel, ConfigDict

class PartCreate(BaseModel):
    name: str
    sku: str
    price: float
    stock: int = 0

class PartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    sku: str
    price: float
    stock: int

class StockOperation(BaseModel):
    quantity: int
