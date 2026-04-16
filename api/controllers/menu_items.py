from .crud import create_item, delete_item, read_all_items, read_one_item, update_item
from ..models import menu_items as model



def create(db, request):
    return create_item(db, model.MenuItem, request)



def read_all(db, category: str | None = None, available_only: bool = False):
    def query_modifier(query):
        if category:
            query = query.filter(model.MenuItem.food_category.ilike(f"%{category}%"))
        if available_only:
            query = query.filter(model.MenuItem.is_available.is_(True))
        return query

    return read_all_items(db, model.MenuItem, query_modifier=query_modifier)



def read_one(db, item_id: int):
    return read_one_item(db, model.MenuItem, item_id)



def update(db, item_id: int, request):
    return update_item(db, model.MenuItem, item_id, request)



def delete(db, item_id: int):
    return delete_item(db, model.MenuItem, item_id)