from . import (
    customers,
    menu_items,
    order_items,
    orders,
    payments,
    promotions,
    recipes,
    resources,
    reviews,
)
from ..dependencies.database import Base, engine



def index():
    Base.metadata.create_all(bind=engine)