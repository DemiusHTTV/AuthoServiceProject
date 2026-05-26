class InventoryModel(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)        # Название (например, "Масло моторное 5W-30")
    sku = Column(String, unique=True, nullable=False) # Артикул (например, "OIL-5W30-CH")
    quantity = Column(Integer, default=0)        # Количество (например, 24)
    status = Column(String, default="В наличии")  # "В наличии", "Заканчивается", "Нет на складе"


# --- РОУТ ДЛЯ API ---
# (Вставляй в свой существующий APIRouter)
@router.get("/inventory")
def get_warehouse_inventory(db: Session = Depends(get_db)):
    """Выгрузка всех остатков со склада для админки Елены"""
    return db.query(InventoryModel).all()