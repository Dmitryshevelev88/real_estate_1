from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.import_batch import ImportBatch
from app.services.imports.batch_service import start_batch
from app.services.imports.import_orchestrator import run_catalog_csv_import

router = APIRouter(prefix="/admin/import-batches", tags=["admin-imports"])


@router.post("/upload")
def upload_catalog_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing")

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    batch = start_batch(db, filename=file.filename, source_type="csv")

    try:
        content = file.file.read()
        result = run_catalog_csv_import(db, batch, content)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Import failed: {exc}")


@router.get("")
def list_import_batches(db: Session = Depends(get_db)):
    items = db.scalars(
        select(ImportBatch).order_by(ImportBatch.id.desc())
    ).all()
    return list(items)


@router.get("/{batch_id}")
def get_import_batch(batch_id: int, db: Session = Depends(get_db)):
    item = db.get(ImportBatch, batch_id)
    if not item:
        raise HTTPException(status_code=404, detail="Import batch not found")
    return item