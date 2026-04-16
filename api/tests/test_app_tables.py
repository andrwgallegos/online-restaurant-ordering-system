from sqlalchemy import inspect

from api.dependencies.database import engine
from api.main import app



def test_app_loads():
    assert app.title == "Online Restaurant Ordering System API"



def test_all_core_tables_exist():
    inspector = inspect(engine)
    expected_tables = {
        "customers",
        "menu_items",
        "resources",
        "recipes",
        "promotions",
        "orders",
        "order_items",
        "payments",
        "reviews",
    }

    assert expected_tables.issubset(set(inspector.get_table_names()))