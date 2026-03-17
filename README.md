# inventory

**Inventory microservice** for ShopWorthy — Python 3.11 + FastAPI, PostgreSQL. Manages stock levels, reserves, webhooks, and export endpoints.

Part of the [ShopWorthy](https://github.com/ShopWorthy) organization.

## Technology

| Item | Choice |
|------|--------|
| Language | Python 3.11 |
| Framework | FastAPI |
| Database | PostgreSQL (via `psycopg2`) |
| HTTP Client | `requests` |

## Prerequisites

- Python 3.11+
- pip

## Setup

```bash
pip install -r requirements.txt
```

## Run (development)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

The service will be available at **http://localhost:5000**. It expects PostgreSQL when running with a database.

## Docker

```bash
docker build -t shopworthy-inventory .
docker run -p 5000:5000 shopworthy-inventory
```

## Port

| Environment | Port |
|-------------|------|
| FastAPI | 5000 |

## Related Repositories

- [api](https://github.com/ShopWorthy/api) — Primary API (calls this service)
- [admin](https://github.com/ShopWorthy/admin) — Admin panel (shares PostgreSQL)
- [infra](https://github.com/ShopWorthy/infra) — Full stack via Docker Compose
