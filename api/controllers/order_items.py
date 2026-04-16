from .crud import create_item, delete_item, read_all_items, read_one_item, update_item
from ..models import order_items as model



def create(db, request):
    return create_item(db, model.OrderItem, request)



def read_all(db):
    return read_all_items(db, model.OrderItem)



def read_one(db, item_id: int):
    return read_one_item(db, model.OrderItem, item_id)



def update(db, item_id: int, request):
    return update_item(db, model.OrderItem, item_id, request)



def delete(db, item_id: int):
    return delete_item(db, model.OrderItem, item_id)