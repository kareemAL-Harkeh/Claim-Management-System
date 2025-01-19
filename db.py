# Run This file to create the DB
from models import Base
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./test.db" 
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)