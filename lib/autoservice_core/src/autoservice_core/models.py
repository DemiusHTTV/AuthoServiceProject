from pydantic import BaseModel

class Part(BaseModel):
    id: int
    name: str
    count: int
    price: float

class OrderItem(BaseModel):
    part_id: int
    qty: int
