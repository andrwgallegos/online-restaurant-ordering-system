from datetime import date, datetime, timedelta
from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from api.controllers import checkout as checkout_controller


class _PromoStub:
    def __init__(self, code="SAVE10", discount_type="percentage", discount_value=10, is_active=True, expired=False):
        self.id = 1
        self.code = code
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.is_active = is_active
        self.expiration_date = date.today() - timedelta(days=1) if expired else date.today() + timedelta(days=10)



def test_calculate_discount_percentage():
    promo = _PromoStub(discount_type="percentage", discount_value=10)
    result = checkout_controller._calculate_discount(promo, Decimal("100.00"))
    assert result == Decimal("10.00")



def test_calculate_discount_flat_capped_at_subtotal():
    promo = _PromoStub(discount_type="flat", discount_value=50)
    result = checkout_controller._calculate_discount(promo, Decimal("20.00"))
    assert result == Decimal("20.00")



def test_calculate_discount_no_promo_returns_zero():
    result = checkout_controller._calculate_discount(None, Decimal("50.00"))
    assert result == Decimal("0.00")



def test_resolve_promotion_rejects_expired():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = _PromoStub(expired=True)
    with pytest.raises(HTTPException) as info:
        checkout_controller._resolve_promotion(db, "EXPIRED")
    assert info.value.status_code == 400



def test_resolve_promotion_rejects_inactive():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = _PromoStub(is_active=False)
    with pytest.raises(HTTPException) as info:
        checkout_controller._resolve_promotion(db, "INACTIVE")
    assert info.value.status_code == 400



def test_resolve_promotion_returns_none_when_no_code():
    db = MagicMock()
    assert checkout_controller._resolve_promotion(db, None) is None



def test_resolve_promotion_404_when_missing():
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as info:
        checkout_controller._resolve_promotion(db, "NOPE")
    assert info.value.status_code == 404
