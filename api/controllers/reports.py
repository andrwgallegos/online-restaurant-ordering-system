from datetime import date, datetime, time
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from ..models import menu_items as menu_item_model
from ..models import order_items as order_item_model
from ..models import orders as order_model
from ..models import payments as payment_model
from ..models import recipes as recipe_model
from ..models import resources as resource_model
from ..models import reviews as review_model



def _detail(exc: SQLAlchemyError) -> str:
    return str(getattr(exc, "orig", exc))



def low_stock_resources(db, threshold: float = 10.0):
    try:
        rows = (
            db.query(resource_model.Resource)
            .filter(resource_model.Resource.stock_amount <= threshold)
            .all()
        )
        return [
            {
                "id": row.id,
                "resource_name": row.resource_name,
                "stock_amount": float(row.stock_amount),
                "unit": row.unit,
                "threshold": threshold,
            }
            for row in rows
        ]
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def insufficient_for_order(db, order_id: int):
    try:
        order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found!")

        shortages = []
        for item in order.order_items:
            recipes = (
                db.query(recipe_model.Recipe)
                .filter(recipe_model.Recipe.menu_item_id == item.menu_item_id)
                .all()
            )
            for recipe in recipes:
                resource = (
                    db.query(resource_model.Resource)
                    .filter(resource_model.Resource.id == recipe.resource_id)
                    .first()
                )
                if not resource:
                    continue
                needed = Decimal(recipe.amount_required) * Decimal(item.quantity)
                if Decimal(resource.stock_amount) < needed:
                    shortages.append(
                        {
                            "menu_item_id": item.menu_item_id,
                            "resource_id": resource.id,
                            "resource_name": resource.resource_name,
                            "needed": float(needed),
                            "available": float(resource.stock_amount),
                            "unit": resource.unit,
                        }
                    )
        return {"order_id": order_id, "has_shortage": len(shortages) > 0, "shortages": shortages}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def daily_revenue(db, target_date: date):
    try:
        start = datetime.combine(target_date, time.min)
        end = datetime.combine(target_date, time.max)
        total = (
            db.query(func.coalesce(func.sum(payment_model.Payment.amount), 0))
            .filter(payment_model.Payment.transaction_status == "completed")
            .filter(payment_model.Payment.paid_at >= start)
            .filter(payment_model.Payment.paid_at <= end)
            .scalar()
        )
        order_count = (
            db.query(func.count(func.distinct(order_model.Order.id)))
            .filter(order_model.Order.order_date >= start)
            .filter(order_model.Order.order_date <= end)
            .scalar()
        )
        return {
            "date": target_date.isoformat(),
            "total_revenue": float(total or 0),
            "order_count": int(order_count or 0),
        }
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def orders_in_range(db, start_date: date, end_date: date):
    try:
        start = datetime.combine(start_date, time.min)
        end = datetime.combine(end_date, time.max)
        return (
            db.query(order_model.Order)
            .filter(order_model.Order.order_date >= start)
            .filter(order_model.Order.order_date <= end)
            .order_by(order_model.Order.order_date.desc())
            .all()
        )
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def dish_review_summary(db, min_reviews: int = 1):
    try:
        rows = (
            db.query(
                menu_item_model.MenuItem.id,
                menu_item_model.MenuItem.name,
                func.count(review_model.Review.id).label("review_count"),
                func.coalesce(func.avg(review_model.Review.rating), 0).label("average_rating"),
            )
            .outerjoin(review_model.Review, review_model.Review.menu_item_id == menu_item_model.MenuItem.id)
            .group_by(menu_item_model.MenuItem.id, menu_item_model.MenuItem.name)
            .having(func.count(review_model.Review.id) >= min_reviews)
            .order_by(func.avg(review_model.Review.rating).asc())
            .all()
        )
        return [
            {
                "menu_item_id": row[0],
                "menu_item_name": row[1],
                "review_count": int(row[2]),
                "average_rating": round(float(row[3]), 2),
            }
            for row in rows
        ]
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc