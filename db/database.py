from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import DBConfig

from models.base import Base
from models.sight import SightModel, SightPicture
from models.users import UserModel


db_condig = DBConfig()


engine = create_engine(f"postgresql+psycopg2://{db_condig.user}:{db_condig.password}@{db_condig.host}:{db_condig.port}/{db_condig.name}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db():
    Base.metadata.create_all(bind=engine)