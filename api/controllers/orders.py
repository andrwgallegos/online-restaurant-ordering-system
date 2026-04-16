import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from .crud import create_item, delete_item, read_all_items, read_one_item, update_item
from ..models import orders as model



def create(db, request):
    tracking_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
    extra_values = {"tracking_number": tracking_number, "order_status": "pending"}
    return create_item(db, model.Order, request, extra_values=extra_values)



def read_all(db):
    return read_all_items(db, model.Order)



def read_one(db, item_id: int):
    return read_one_item(db, model.Order, item_id)



def read_by_tracking(db, tracking_number: str):
    try:
        item = db.query(model.Order).filter(model.Order.tracking_number == tracking_number).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tracking number not found!")
        return item
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(getattr(exc, "orig", exc))) from exc



def update(db, item_id: int, request):
    return update_item(db, model.Order, item_id, request)



def delete(db, item_id: int):
    return delete_item(db, model.Order, item_id)