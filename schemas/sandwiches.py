from pydantic import BaseModel, ConfigDict


class SandwichBase(BaseModel):
    sandwich_name: str
    price: float


class Sandwich(SandwichBase):
    id: int
    model_config = ConfigDict(from_attributes=True)