from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ..controllers import reports as controller
from ..dependencies.database import get_db
from ..schemas import orders as order_schema

router = APIRouter(tags=["Reports"], prefix="/reports")


@router.get("/low-stock")
def low_stock(threshold: float = 10.0, db: Session = Depends(get_db)):
    return controller.low_stock_resources(db, threshold=threshold)


@router.get("/orders/{order_id}/insufficient-resources")
def insufficient_resources(order_id: int, db: Session = Depends(get_db)):
    return controller.insufficient_for_order(db, order_id=order_id)


@router.get("/revenue/daily")
def revenue_daily(target_date: date = Query(..., alias="date"), db: Session = Depends(get_db)):
    return controller.daily_revenue(db, target_date=target_date)


@router.get("/orders/range", response_model=list[order_schema.Order])
def orders_in_range(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
):
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date must be on or before end_date",
        )
    return controller.orders_in_range(db, start_date=start_date, end_date=end_date)


@router.get("/dishes/review-summary")
def dish_review_summary(min_reviews: int = 1, db: Session = Depends(get_db)):
    return controller.dish_review_summary(db, min_reviews=min_reviews)