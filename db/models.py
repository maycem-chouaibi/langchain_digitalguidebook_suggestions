from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from .connect import get_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    phone_ext = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    dob = Column(String, nullable=False)
    gender = Column(String, nullable=False)

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

