import os

os.environ.setdefault("DB_ENGINE", "sqlite")
os.environ.setdefault(
    "SQLITE_PATH",
    os.path.join(os.path.dirname(__file__), "test_restaurant.db"),
)
