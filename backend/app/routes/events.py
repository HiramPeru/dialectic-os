from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.event import Event
from app.services.clustering import cluster_articles

router = APIRouter()

@router.post("/cluster")
def cluster(db: Session = Depends(get_db)):
    return cluster_articles(db)

@router.get("")
def list_events(db: Session = Depends(get_db)):
    rows = db.query(Event).all()

    return [
        {
            "id": row.id,
            "title": row.title,
            "topic": row.topic,
            "article_count": row.article_count
        }
        for row in rows
    ]
