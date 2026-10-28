from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base



engine = create_engine(
    "sqlite:///database.db", connect_args={"autocommit": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db


def create_db():
    Base.metadata.create_all(bind=engine)