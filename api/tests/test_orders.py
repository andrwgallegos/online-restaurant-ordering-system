from unittest.mock import MagicMock

from api.controllers import orders as controller


class DummyRequest:
    customer_id = 1
    promotion_id = None
    fulfillment_type = "delivery"
    subtotal = 24.50
    discount_amount = 2.50
    total_price = 22.00
    delivery_address = "123 Main St"
    special_instructions = "Leave at door"

    def model_dump(self, exclude_none=True):
        data = {
            "customer_id": self.customer_id,
            "promotion_id": self.promotion_id,
            "fulfillment_type": self.fulfillment_type,
            "subtotal": self.subtotal,
            "discount_amount": self.discount_amount,
            "total_price": self.total_price,
            "delivery_address": self.delivery_address,
            "special_instructions": self.special_instructions,
        }
        if exclude_none:
            return {key: value for key, value in data.items() if value is not None}
        return data



def test_create_order():
    db = MagicMock()
    request = DummyRequest()

    result = controller.create(db, request)

    assert result.customer_id == 1
    assert result.fulfillment_type == "delivery"
    assert result.total_price == 22.00
    assert result.delivery_address == "123 Main St"
    assert result.special_instructions == "Leave at door"
    assert result.order_status == "pending"
    assert result.tracking_number.startswith("ORD-")

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()