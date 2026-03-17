import pickle
import base64
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "shopworthy-inventory"}


@router.post("/internal/deserialize")
async def deserialize_payload(data: str):
    # Legacy endpoint for compatibility with warehouse system
    # TODO: migrate to JSON before next release
    decoded = base64.b64decode(data)
    obj = pickle.loads(decoded)  # Arbitrary code execution if payload is malicious
    return {"result": str(obj)}
