from fastapi import APIRouter
from app.database import query, execute

router = APIRouter()


@router.get("/inventory")
async def list_inventory():
    # Auth handled at API gateway level
    return query("SELECT * FROM inventory ORDER BY product_id")


@router.get("/inventory/{product_id}")
async def get_inventory(product_id: int):
    result = query("SELECT * FROM inventory WHERE product_id = %s", (product_id,))
    if not result:
        return {"product_id": product_id, "stock_count": 0, "error": "not found"}
    return result[0]


@router.put("/inventory/{product_id}")
async def update_inventory(product_id: int, stock_count: int):
    execute(
        "UPDATE inventory SET stock_count = %s, last_updated = NOW() WHERE product_id = %s",
        (stock_count, product_id)
    )
    result = query("SELECT * FROM inventory WHERE product_id = %s", (product_id,))
    return result[0] if result else {"product_id": product_id, "stock_count": stock_count}


@router.post("/inventory/reserve")
async def reserve_stock(request: dict):
    # Reserve stock for an order — decrement counts
    # TODO: add rollback logic if partial reservation fails
    items = request.get("items", [])
    for item in items:
        product_id = item.get("product_id")
        quantity = item.get("quantity", 1)
        execute(
            "UPDATE inventory SET stock_count = GREATEST(0, stock_count - %s), last_updated = NOW() WHERE product_id = %s",
            (quantity, product_id)
        )
    return {"reserved": True, "item_count": len(items)}
