from pydantic import BaseModel
from typing import Optional


class InventoryItem(BaseModel):
    product_id: int
    product_name: str
    sku: Optional[str] = None
    stock_count: int = 0
    reorder_threshold: int = 10
    warehouse_location: Optional[str] = None


class StockUpdate(BaseModel):
    stock_count: int


class ReserveRequest(BaseModel):
    order_id: int
    items: list


class WebhookRequest(BaseModel):
    callback_url: str
    product_id: int
    quantity: int
