from typing import Annotated
from fastapi import Depends ,FastAPI

from sqlmodel import SQLModel, create_engine, Session ,select
import os
from dotenv import load_dotenv
from model import ChatRoom

load_dotenv()

Database_url=os.getenv("MYSQL_URI")

engine=create_engine(Database_url,echo=True)

def create_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)
    print("✓ Tables created successfully!")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# Add ping function
def ping_database():
    """Test database connection"""
    try:
        # Get raw DBAPI connection to avoid greenlet/async issues
        raw_conn = engine.raw_connection()
        cursor = raw_conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        raw_conn.close()
        
        if result and result[0] == 1:
            print("✓ Database connection successful!")
            return True
        else:
            print("✗ Database connection failed!")
            return False
    except Exception as e:
        print(f"✗ Database connection error: {e}")
        return False

# Test the connection when running directly
if __name__ == "__main__":
    if ping_database():
        create_tables()