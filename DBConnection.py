from typing import Annotated
from fastapi import Depends ,FastAPI

from sqlmodel import SQLModel, create_engine, Session ,select
import os
from dotenv import load_dotenv
from model import ChatRoom

load_dotenv()

Database_url=os.getenv("DATABASE_URL")

engine=create_engine(Database_url,echo=True)

def create_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)
    print("✓ Tables created successfully!")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

