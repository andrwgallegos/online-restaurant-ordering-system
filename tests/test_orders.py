from unittest.mock import MagicMock

from api.controllers import orders as controller


class DummyRequest:
    customer_name = "John Doe"
    customer_phone = "7045551111"
    customer_address = "123 Main St"
    order_type = "delivery"
    description = "No onions"


def test_create_order():
    db = MagicMock()
    request = DummyRequest()

    result = controller.create(db, request)

    assert result.customer_name == "John Doe"
    assert result.customer_phone == "7045551111"
    assert result.customer_address == "123 Main St"
    assert result.order_type == "delivery"
    assert result.description == "No onions"

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()