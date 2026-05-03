from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..controllers import checkout as controller
from ..dependencies.database import get_db
from ..schemas import checkout as schema
from ..schemas import orders as order_schema

router = APIRouter(tags=["Checkout"], prefix="/checkout")


@router.post("/", response_model=order_schema.Order)
def guest_checkout(request: schema.CheckoutRequest, db: Session = Depends(get_db)):
    return controller.guest_checkout(db=db, request=request)


@router.post("/{order_id}/apply-promotion", response_model=order_schema.Order)
def apply_promotion(order_id: int, request: schema.ApplyPromotionRequest, db: Session = Depends(get_db)):
    return controller.apply_promotion(db=db, order_id=order_id, code=request.code)
