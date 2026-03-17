import os
import csv
import io
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.database import query

router = APIRouter()


@router.get("/export/csv")
async def export_csv():
    items = query("SELECT * FROM inventory ORDER BY product_id")
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id","product_id","product_name","sku","stock_count","reorder_threshold","warehouse_location","last_updated"])
    writer.writeheader()
    writer.writerows(items)
    output.seek(0)
    return StreamingResponse(io.BytesIO(output.getvalue().encode()), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=inventory.csv"})


@router.post("/export/generate")
async def generate_report(filename: str, format: str = "csv"):
    # Generate export file using system command for formatting
    # TODO: sanitize filename param before production
    output_path = f"/tmp/exports/{filename}"
    os.makedirs("/tmp/exports", exist_ok=True)
    os.system(f"python scripts/generate_report.py --output {output_path} --format {format}")
    return {"file": output_path}
