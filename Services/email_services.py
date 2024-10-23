from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from typing import List
from dotenv import load_dotenv, dotenv_values
from fastapi import HTTPException
import os

# Email Configuration with .env file
creds = dotenv_values(".env")

config_email = ConnectionConfig(

    MAIL_USERNAME=creds['EMAIL'],
    MAIL_PASSWORD=creds['PASS'],
    MAIL_FROM=creds['EMAIL'],
    MAIL_PORT=465,  # Usually 587 for TLS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True

)

# Pydantic model for Email Data
class EmailSchema(BaseModel):
    supplier_email: str
    supplier_name: str
    product_name: str
    company_name: str

async def send_email(supplier_email: str, supplier_name: str, product_name: str, company_name: str ):
    subject = f"Thank you for your Business! {company_name}"
    body = (
        f"Dear {supplier_name}, \n\n"
        f"Thank you for listing you product {product_name} with you \n\n"
        f"\n"
        f"Best Regards, \n"
        "IM Team"
    )
    message = MessageSchema(
        subject=subject,
        recipients=[supplier_email],  # List of recipients
        body=body,
        subtype="plain"
    )

    fm = FastMail(config_email)
    try:
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")
