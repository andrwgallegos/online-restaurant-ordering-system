from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResourceBase(BaseModel):
    resource_name: str
    stock_amount: float
    unit: str


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    resource_name: Optional[str] = None
    stock_amount: Optional[float] = None
    unit: Optional[str] = None


class Resource(ResourceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)