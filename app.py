from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from SQL.models import supplier_pydantic, supplier_pydanticInput, Supplier
from SQL.models import product_pydantic, product_pydanticInput, Product
from tortoise import Tortoise
from fastapi.responses import HTMLResponse, RedirectResponse
from Services.email_services import EmailSchema, send_email
import logging
from tortoise.exceptions import DoesNotExist


#initilize the FastAPI app
IMapp = FastAPI()

# Tortoise-ORM
async def init_db():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",
        modules={"models":["SQL.models"]}
    )
    await Tortoise.generate_schemas(safe=True)


# Registering the Tortoise ORM using the config.py file
register_tortoise(
    IMapp,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["SQL.models"]},
    generate_schemas=True,
    add_exception_handlers=True
)


@IMapp.get("/", response_class = RedirectResponse)
async def redirect_to_myapp():
    return RedirectResponse(url="/Inventory-Management")

@IMapp.get("/Inventory-Management")
async def homepage():
    return {"Message" : "This is the Home Page"}


@IMapp.get("/about-us")
def about():
    return {"Message" : "This is the About Page"}


# create add supplier api
@IMapp.post("/supplier/create")
async def create_supplier(supplier_info:supplier_pydanticInput):
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))
    response = await supplier_pydantic.from_tortoise_orm(supplier_obj)
    return {"Status":"200", "data":response }


# get all supplier api
@IMapp.get("/supplier")
async def get_all_supplier():
    try:
        response = await supplier_pydantic.from_queryset(Supplier.all())
        return {"Status":"200", "data":response }
    except Exception as e:
        print(f"Error Found : {e}")


# get supplier by id api
@IMapp.get("/supplier/{supplier_id}")
async def get_specific_supplier(supplier_id: int):
    try:
        response = await supplier_pydantic.from_queryset_single(Supplier.get(id=supplier_id))
        return {"Status":"200", "data":response }
    except Exception as e:
        print(f"Error Found - {e}")
        return {"Status":"Error", "data":e}


# update supplier by id api
@IMapp.put("/supplier/{supplier_id}")
async def update_supplier(supplier_id: int, update_info:supplier_pydanticInput):
    supplier = await Supplier.get(id=supplier_id)
    update_info = update_info.dict(exclude_unset=True)
    supplier.name = update_info['name']
    supplier.company = update_info["company"]
    supplier.email = update_info["email"]
    supplier.phone = update_info["phone"]
    await supplier.save()
    response = await supplier_pydantic.from_tortoise_orm(supplier)
    return {"Status":"200", "data":response }


# delete supplier by id api
@IMapp.delete("/supplier/{supplier_id}")
async def delete_supplier(supplier_id: int):
    supplier_delete = await Supplier.filter(id=supplier_id).first()
    supplier_name = supplier_delete.name
    await supplier_delete.delete()
    return {"Status":"200", "message": f"Supplier'{supplier_name}' deleted Successfully"}


# ------------------------------------------------------------------------------------------------------- #

# Add Product api
@IMapp.post("/product/create/{supplier_id}")

async def create_product(supplier_id: int, product_info: product_pydanticInput):
    try:
        supplier = await Supplier.get(id=supplier_id)
        product_info = product_info.dict(exclude_unset=True)
        product_info['revenue'] += product_info['quantity_sold'] * product_info['unit_price']
        product_obj = await Product.create(**product_info, supplied_by = supplier)
        response = await product_pydantic.from_tortoise_orm(product_obj)
        return {"Status":"200", "data":response }
    except HTTPException as http_error:
        logging.error(f"Error : {http_error.detail}")
        raise
    except Exception as e:
        logging.error(f"Unexpected Error : {str(e)}")
        print(f"str{e}")
        raise


# Get All Product api
@IMapp.get("/product")
async def get_all_products():
    response = await product_pydantic.from_queryset(Product.all())
    return{"Status":"200", "data":response }

# Get Product by id api
@IMapp.get("/product/{product_id}")
async def get_specific_product(product_id: int):
    response = await product_pydantic.from_queryset_single(Product.get(id=product_id))
    return {"Status":"200", "data":response }

# Update Product details api
@IMapp.put("/product/{product_id}")
async def update_product(product_id: int, update_info: product_pydanticInput):
    product = await Product.get(id=product_id)
    update_info = update_info.dict(exclude_unset=True)
    product.name = update_info['name']
    product.quantity_in_stock = update_info['quantity_in_stock']
    product.sold = update_info['quantity_sold']
    product.unit_price = update_info['unit_price']
    product.revenue = (update_info['quantity_sold'] * update_info['unit_price']) + update_info['revenue']
    await product.save()
    response = await product_pydantic.from_tortoise_orm(product)
    return {"Status":"200", "data": "Data Updated Successfully" }

# Delete product api
@IMapp.delete("/product/{product_id}")
async def delete_product(product_id: int):
    product_delete = await Product.filter(id=product_id).first()
    product_name = product_delete.name
    response = await product_delete.delete()
    return {"Status": "200", "Message": f"Product '{product_name}' deleted Successfully"}


# Email send API
@IMapp.post("/send-email/{product_id}")
async def send_email_endpoint(product_id: int):
    try:
        product = await Product.get(id=product_id).prefetch_related('supplied_by')
        supplier = await product.supplied_by

        await send_email(
            supplier_email=supplier.email,
            supplier_name=supplier.name,
            product_name=product.name,
            company_name=supplier.company
        )
        return{"Status":"200", "Message": f"Email Successfully sent to {supplier.name}"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")







