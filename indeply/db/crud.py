from typing import TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from connect import create_session
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)

def create_record(model: Type[T], **kwargs) -> T:
    with create_session() as session:
        record = model(**kwargs)
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

def get_record_by_id(model: Type[T], record_id: int) -> Optional[T]:
    with create_session() as session:
        return session.get(model, record_id)

def get_all_records(model: Type[T]) -> List[T]:
    with create_session() as session:
        return session.query(model).all()

def update_record(model: Type[T], record_id: int, **kwargs) -> Optional[T]:
    with create_session() as session:
        record = session.get(model, record_id)
        if not record:
            return None
        for key, value in kwargs.items():
            if hasattr(record, key):
                setattr(record, key, value)
        session.commit()
        session.refresh(record)
        return record

def delete_record(model: Type[T], record_id: int) -> bool:
    with create_session() as session:
        record = session.get(model, record_id)
        if not record:
            return False
        session.delete(record)
        session.commit()
        return True
