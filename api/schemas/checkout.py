from typing import List, Optional

from pydantic import BaseModel, EmailStr


class CheckoutCustomer(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    address: str


class CheckoutItem(BaseModel):
    menu_item_id: int
    quantity: int


class CheckoutPayment(BaseModel):
    payment_type: str
    card_last4: Optional[str] = None


class CheckoutRequest(BaseModel):
    customer: CheckoutCustomer
    items: List[CheckoutItem]
    fulfillment_type: str
    delivery_address: str
    special_instructions: Optional[str] = None
    promotion_code: Optional[str] = None
    payment: Optional[CheckoutPayment] = None


class ApplyPromotionRequest(BaseModel):
    code: str
