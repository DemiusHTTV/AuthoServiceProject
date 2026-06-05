
from typing import List
from .models import OrderItem, Part

def calculate_total_price(items: List[OrderItem], parts_db: List[Part]) -> float:
    total = 0.0
    for item in items:
        if item.qty < 0:
            raise ValueError("Quantity must be non-negative")
            
        part = next((p for p in parts_db if p.id == item.part_id), None)
        if not part:
            raise ValueError(f"Part with id {item.part_id} not found in warehouse")
        if item.qty > part.quantity:
            raise ValueError(f"Not enough parts in warehouse for {part.name}")
        total += item.qty * part.price
    return total
