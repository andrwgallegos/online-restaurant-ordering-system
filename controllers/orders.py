import uuid

from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import orders as model


def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        customer_phone=request.customer_phone,
        customer_address=request.customer_address,
        order_type=request.order_type,
        description=request.description,
        tracking_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
        status="pending"
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e

    return new_item


def read_all(db: Session):
    try:
        return db.query(model.Order).all()
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        return item
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e


def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        current = item.first()
        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        update_data = request.model_dump(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
        return item.first()
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e


def delete(db: Session, item_id: int):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        current = item.first()
        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e