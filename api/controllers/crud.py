from fastapi import HTTPException, Response, status
from sqlalchemy.exc import SQLAlchemyError



def _detail(exc: SQLAlchemyError) -> str:
    return str(getattr(exc, "orig", exc))



def create_item(db, model_class, request, extra_values=None):
    data = request.model_dump(exclude_none=True)
    if extra_values:
        data.update(extra_values)
    new_item = model_class(**data)
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def read_all_items(db, model_class, query_modifier=None):
    try:
        query = db.query(model_class)
        if query_modifier:
            query = query_modifier(query)
        return query.all()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def read_one_item(db, model_class, item_id: int):
    try:
        item = db.query(model_class).filter(model_class.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        return item
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def update_item(db, model_class, item_id: int, request):
    try:
        query = db.query(model_class).filter(model_class.id == item_id)
        current = query.first()
        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.model_dump(exclude_unset=True)
        query.update(update_data, synchronize_session=False)
        db.commit()
        return query.first()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def delete_item(db, model_class, item_id: int):
    try:
        query = db.query(model_class).filter(model_class.id == item_id)
        current = query.first()
        if not current:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc