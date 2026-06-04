from .models import Part, OrderItem
from typing import List

def calculate_total_price(items: List[OrderItem], parts_db: List[Part]) -> float:
    total = 0.0
    for item in items:
        if item.qty < 0:
            raise ValueError("Quantity must be non-negative")
            
        part = next((p for p in parts_db if p.id == item.part_id), None)
        if not part:
            raise ValueError(f"Part with ID {item.part_id} not found")
            
        if part.count < item.qty:
            raise ValueError(f"Not enough parts in stock for ID {item.part_id}")
            
        total += part.price * item.qty
    return total
