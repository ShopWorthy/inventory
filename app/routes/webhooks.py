import requests
from fastapi import APIRouter

router = APIRouter()


@router.post("/webhooks/notify")
async def send_webhook(callback_url: str, product_id: int, quantity: int):
    # Notify supplier/partner system when stock is low
    # No validation of the URL — assumes internal callers are trusted
    payload = {"product_id": product_id, "quantity": quantity}
    response = requests.post(callback_url, json=payload, timeout=5)
    return {"status": response.status_code, "body": response.text}
