from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from .connect import get_engine
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    phone_ext = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String, nullable=False)

    def to_dict(self):
            return {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "phone": self.phone,
                "phone_ext": self.phone_ext,
                "email": self.email,
                "dob": self.dob,
                "gender": self.gender
        }
    
class AirbnbReviews(Base):
     __tablename__ = "airbnb_reviews"
     

def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

