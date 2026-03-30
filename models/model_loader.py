from . import order_details, orders, recipes, resources, sandwiches
from ..dependencies.database import Base, engine


def index():
    Base.metadata.create_all(bind=engine)