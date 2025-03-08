from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from functools import lru_cache
from sqlalchemy.orm import scoped_session

load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB_NAME")
USERNAME = os.getenv("POSTGRES_USERNAME")
DRIVER = os.getenv("POSTGRES_DRIVER")
HOST = os.getenv("POSTGRES_HOST")
PASSWORD = os.getenv("POSTGRES_PWD")
PORT = os.getenv("POSTGRES_PORT")

@lru_cache(maxsize=1)
def get_engine():
    url = URL.create(
        drivername=DRIVER,
        username=USERNAME,
        host=HOST,
        database=DB_NAME,
        port=PORT,
        password=PASSWORD
    )
    engine = create_engine(url)

    return engine


def create_session():
    try:
        engine = get_engine()
        Session = sessionmaker(bind=engine) 
        session = Session()

        return session
    
    except Exception as e:
        raise ConnectionError("Failed to create session: {e}")
    
def close_connection(engine):
    Session = scoped_session(sessionmaker(bind=engine))
    Session.remove()

    # Then dispose of the engine
    engine.dispose()


