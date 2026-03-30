from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import order_details as model


def create(db: Session, request):
    new_item = model.OrderDetail(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e


def read_all(db: Session):
    try:
        return db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        return item
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e


def update(db: Session, item_id: int, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
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
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
        current = item.first()
        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        item.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as e:
        detail = str(getattr(e, "orig", e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail) from e