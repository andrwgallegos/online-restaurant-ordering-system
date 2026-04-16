from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import conf



def build_database_url() -> str:
    if conf.db_engine == "mysql":
        return (
            f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}"
            f"@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
        )

    sqlite_path = Path(conf.sqlite_path)
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{sqlite_path}"


SQLALCHEMY_DATABASE_URL = build_database_url()

engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()