from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from fastapi import Depends

from typing import Annotated

from ..db.database import engine


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db

#Зависимость для обращения в базу данных.
DB = Annotated[Session, Depends(get_db)]