from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .src.sql.database import dbEngine, Base, get_db

#initilize the FastAPI app
IMapp = FastAPI()

Base.metadata.create_all(bind=dbEngine)

# Home Page api 
@IMapp.get("/")
def Homepage():
    return {"Message" : "This is the Home Page"}

# Route Using database
@IMapp.get("/")
def read_root(db: Session = Depends(get_db)):
    return{"message": "Database is working"}

