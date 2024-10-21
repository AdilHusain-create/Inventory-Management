from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

# Defining Product Model Class
class Product(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, nullable=False)
    quantity_in_stock = fields.IntField(max_digit=10, default=0)
    quantity_sold = fields.IntField(max_digit=10 ,default=0)
    unit_price = fields.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    revenue = fields.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    supplied_by = fields.ForeignKeyField('models.Supplier', related_name="goods_supplied")

#Defining Supplier Model Class
class Supplier(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=100, nullable=False)
    company = fields.CharField(max_length=100, nullable=False)
    email = fields.CharField(max_length=100, nullable=False)
    phone = fields.BigIntField(max_length=20, nullable=False)


# Creating Pydantic Models which will create tables automatically
# Product Pydantic Model
product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticInput = pydantic_model_creator(Product, name="ProductInput", exclude_readonly=True)


# Supplier Pydantic Model
supplier_pydantic = pydantic_model_creator(Supplier, name="Supplier")
supplier_pydanticInput = pydantic_model_creator(Supplier, name="SupplierInput", exclude_readonly=True)