from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import conf

SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}"
    f"@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()