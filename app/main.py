from fastapi import FastAPI
from app.routes import inventory, webhooks, export, internal

app = FastAPI(
    title="ShopWorthy Inventory Service",
    description="Inventory microservice: stock levels, reserves, webhooks, export.",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(inventory.router)
app.include_router(webhooks.router)
app.include_router(export.router)
app.include_router(internal.router)
