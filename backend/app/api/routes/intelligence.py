from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.db.models.article import Article
from app.intelligence.analysis.consensus import consensus_from_articles
from app.intelligence.analysis.divergence import divergence_from_articles
from app.intelligence.analysis.briefing import executive_briefing

router = APIRouter()

@router.get("/{keyword}")
def analyze_event(keyword: str, db: Session = Depends(get_db)):
    rows = db.query(Article).all()

    related = [
        r for r in rows
        if keyword.lower() in r.title.lower()
    ]

    if not related:
        raise HTTPException(status_code=404, detail="No matching articles")

    return {
        "keyword": keyword,
        "articles": len(related),
        "consensus": consensus_from_articles(related),
        "divergence": divergence_from_articles(related),
        "briefing": executive_briefing(related)
    }
