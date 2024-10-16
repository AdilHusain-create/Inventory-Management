from pydantic import BaseModel
from typing import Optional, List


# Create Pydantic Models in Torroise ORM
# productPydantic = pydantic_model_creator(Product, name="Product")
# productPydanticInt =pydantic_model_creator(Product, name="ProductInt", exclude_readonly=True)
# supplierPydantic = pydantic_model_creator(Supplier, name="Supplier")
# supplierPydanticInt = pydantic_model_creator(Supplier, name="SupplierInt", exclude_readonly=True)

# Create Pydantic Models in SqlAlchemy

class ProductPydantic(BaseModel):
    id: Optional[int] = None
    name: str
    quantity_in_stock: int = 0
    quantity_sold: int = 0
    unit_price: float = 0.00
    revenue: float = 0.00
    vendor_id: Optional[int] = None

    class Config:
        orm_mode = True


class ProductPydanticInt(BaseModel):
    name: str
    quantity_in_stock: int = 0
    quantity_sold: int = 0
    unit_price: float = 0.00
    revenue: float = 0.00
    vendor_id: Optional[int] = None

    class Config:
        orm_mode = True


class SupplierPydantic(BaseModel):
    id: Optional[int] = None
    name: str
    company: str
    email: str
    phone: int
    goods_supplied: List[ProductPydantic] = []  # List of products supplied

    class Config:
        orm_mode = True


class SupplierPydanticInt(BaseModel):
    name: str
    company: str
    email: str
    phone: int

    class Config:
        orm_mode = True