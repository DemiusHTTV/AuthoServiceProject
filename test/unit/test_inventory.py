import pytest
from autoservice_core import Part, OrderItem, calculate_total_price

def test_calculates_total_for_valid_items():
    parts_db = [
        Part(id=1, name="Фильтр", count=10, price=850.0),
        Part(id=2, name="Колодки", count=4, price=3000.0),
    ]
    items = [
        OrderItem(part_id=1, qty=2),
        OrderItem(part_id=2, qty=1),
    ]
    total = calculate_total_price(items, parts_db)
    assert total == 4700.0

def test_raises_for_negative_quantity():
    parts_db = [Part(id=1, name="Фильтр", count=10, price=850.0)]
    items = [OrderItem(part_id=1, qty=-1)]
    
    with pytest.raises(ValueError) as excinfo:
        calculate_total_price(items, parts_db)
    assert "non-negative" in str(excinfo.value)

def test_raises_for_insufficient_stock():
    parts_db = [Part(id=1, name="Фильтр", count=1, price=850.0)]
    items = [OrderItem(part_id=1, qty=5)]
    
    with pytest.raises(ValueError) as excinfo:
        calculate_total_price(items, parts_db)
    assert "Not enough parts" in str(excinfo.value)
