from sqlalchemy import Column, Float, Integer, String
from warehouse.database.database import Base

class Part(Base):
    __tablename__ = "parts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False, index=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
