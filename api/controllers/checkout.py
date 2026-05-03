import uuid
from datetime import date
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from ..models import customers as customer_model
from ..models import menu_items as menu_item_model
from ..models import order_items as order_item_model
from ..models import orders as order_model
from ..models import payments as payment_model
from ..models import promotions as promotion_model



def _detail(exc: SQLAlchemyError) -> str:
    return str(getattr(exc, "orig", exc))



def _resolve_promotion(db, code):
    if not code:
        return None
    promo = (
        db.query(promotion_model.Promotion)
        .filter(promotion_model.Promotion.code == code)
        .first()
    )
    if not promo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found")
    if not promo.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion is not active")
    if promo.expiration_date < date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion has expired")
    return promo



def _calculate_discount(promo, subtotal):
    if not promo:
        return Decimal("0.00")
    value = Decimal(str(promo.discount_value))
    if promo.discount_type == "percentage":
        return (subtotal * value / Decimal("100")).quantize(Decimal("0.01"))
    return min(value, subtotal).quantize(Decimal("0.01"))



def guest_checkout(db, request):
    try:
        customer = customer_model.Customer(
            full_name=request.customer.full_name,
            email=request.customer.email,
            phone_number=request.customer.phone_number,
            address=request.customer.address,
        )
        db.add(customer)
        db.flush()

        promo = _resolve_promotion(db, request.promotion_code)

        subtotal = Decimal("0.00")
        prepared_items = []
        for line in request.items:
            menu_item = (
                db.query(menu_item_model.MenuItem)
                .filter(menu_item_model.MenuItem.id == line.menu_item_id)
                .first()
            )
            if not menu_item:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Menu item {line.menu_item_id} not found",
                )
            if not menu_item.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Menu item '{menu_item.name}' is unavailable",
                )
            unit_price = Decimal(str(menu_item.price))
            line_total = (unit_price * Decimal(line.quantity)).quantize(Decimal("0.01"))
            subtotal += line_total
            prepared_items.append((menu_item.id, line.quantity, unit_price, line_total))

        discount_amount = _calculate_discount(promo, subtotal)
        total_price = (subtotal - discount_amount).quantize(Decimal("0.01"))

        tracking_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        order = order_model.Order(
            customer_id=customer.id,
            promotion_id=promo.id if promo else None,
            tracking_number=tracking_number,
            order_status="pending",
            fulfillment_type=request.fulfillment_type,
            subtotal=subtotal,
            discount_amount=discount_amount,
            total_price=total_price,
            delivery_address=request.delivery_address,
            special_instructions=request.special_instructions,
        )
        db.add(order)
        db.flush()

        for menu_item_id, quantity, unit_price, line_total in prepared_items:
            db.add(
                order_item_model.OrderItem(
                    order_id=order.id,
                    menu_item_id=menu_item_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    line_total=line_total,
                )
            )

        if request.payment:
            db.add(
                payment_model.Payment(
                    order_id=order.id,
                    payment_type=request.payment.payment_type,
                    transaction_status="completed",
                    amount=total_price,
                    card_last4=request.payment.card_last4,
                    payment_reference=f"PAY-{uuid.uuid4().hex[:10].upper()}",
                )
            )

        db.commit()
        db.refresh(order)
        return order
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc



def apply_promotion(db, order_id: int, code: str):
    try:
        order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        promo = _resolve_promotion(db, code)
        subtotal = Decimal(str(order.subtotal))
        discount_amount = _calculate_discount(promo, subtotal)
        total_price = (subtotal - discount_amount).quantize(Decimal("0.01"))

        order.promotion_id = promo.id
        order.discount_amount = discount_amount
        order.total_price = total_price
        db.commit()
        db.refresh(order)
        return order
    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=_detail(exc)) from exc