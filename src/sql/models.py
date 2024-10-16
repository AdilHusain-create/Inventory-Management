from sqlalchemy import Boolean, Numeric, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
# Pydantic Imports
from pydantic import BaseModel
from typing import Optional, List

# Defining Model Class in Tortoise
# class Product(Base):
    # id = fields.IntField(primary_key=True)
    # name = fields.CharField(max_length=30, nullable=False)
    # quantity_in_stock = fields.IntField(default=0)
    # quantity_solf = fields.IntField(default=0)
    # unit_price = fields.DecimalField(max_digit=10, decimal_places=2,default=0.00)
    # vendors = fields.ForwignKeyField('models.supplier', related_name="goods_supplied")
    # revenue = fields.DeciamlField(max_digits=20, deciaml_places=2, default=0.00)

# Defining Model Class in SQLAlchemy
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    quantityInStock = Column(Integer, default=0)
    quantitySold = Column(Integer, default=0)
    unit_price = Column(Numeric(10,2), default=0.00)
    vendorId = Column(Integer, ForeignKey('suppliers.id'))
    revenue = Column(Numeric(20,2), default=0.00)
    
    # Define relationship with the supplier model
    vendor = relationship('Supplier', back_populates='goods_supplied')

# class Supplier(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=20, nullable=False)
#     company = fields.CharField(max_length=100, nullable=False)
#     email = fields.CharField(max_length=100, nullable=False)
#     phone = fields.intField(max_length=10, nullable=False)

    class Supplier(Base):
        __tablename__ = 'suppliers'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(20), nullable=False)
        company = Column(String(100), nullable=False)
        email = Column(String(100), nullable=False)
        phone = Column(Integer, nullable=False)
        
# Define Relationship with Product
    goods_supplied = relationship('Product', back_populates='vendor')
    
    
