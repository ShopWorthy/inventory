from fastapi import FastAPI
from app.routes import inventory, webhooks, export, internal

# Auth handled at API gateway level
app = FastAPI(title="ShopWorthy Inventory Service", version="1.0.0")

app.include_router(inventory.router)
app.include_router(webhooks.router)
app.include_router(export.router)
app.include_router(internal.router)
