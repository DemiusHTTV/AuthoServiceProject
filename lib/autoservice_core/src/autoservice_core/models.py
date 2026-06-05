from pydantic import BaseModel
from typing import Optional

class Part(BaseModel):
    id: int
    name: str
    article: str
    price: float
    quantity: int
    category: Optional[str] = None

class OrderItem(BaseModel):
    part_id: int
    qty: int
