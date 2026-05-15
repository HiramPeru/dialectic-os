from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.article import Article

router = APIRouter()

@router.get("/")
def list_articles(db: Session = Depends(get_db)):
    rows = db.query(Article).limit(100).all()

    return [
        {
            "id": row.id,
            "source": row.source,
            "title": row.title,
            "url": row.url
        }
        for row in rows
    ]
