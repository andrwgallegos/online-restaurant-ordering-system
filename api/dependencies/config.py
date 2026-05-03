import os
from pathlib import Path


class conf:
    db_engine = os.getenv("DB_ENGINE", "mysql").lower()
    sqlite_path = os.getenv(
        "SQLITE_PATH",
        str(Path(__file__).resolve().parents[1] / "restaurant_ordering.db")
    )
    db_host = os.getenv("DB_HOST", "localhost")
    db_name = os.getenv("DB_NAME", "restaurant_ordering_system")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "password123")
    app_host = os.getenv("APP_HOST", "127.0.0.1")
    app_port = int(os.getenv("APP_PORT", "8000"))