from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# we are "connecting" to a SQLite database (opening a file with the SQLite database).
SQLALCHEMY_DB_URL = 'sqlite:///./sql_app.db'

dbEngine = create_engine(
    SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=dbEngine)

Base = declarative_base()

# Dependency to get the DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

