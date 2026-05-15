from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.ingestion.service import run_ingest

router = APIRouter()

@router.post("/run")
def ingest(db: Session = Depends(get_db)):
    return run_ingest(db)
