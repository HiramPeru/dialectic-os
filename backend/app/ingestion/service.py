import hashlib
import uuid

from sqlalchemy.orm import Session

from app.db.models.article import Article
from app.connectors.rss import RSSConnector

CONNECTORS = [
    RSSConnector("Reuters", "fact_core", "https://feeds.reuters.com/reuters/worldNews", 0.95),
    RSSConnector("AP", "fact_core", "https://feeds.apnews.com/rss/apf-topnews", 0.95),
    RSSConnector("BBC", "western_editorial", "http://feeds.bbci.co.uk/news/world/rss.xml", 0.90),
    RSSConnector("DW", "eu_editorial", "https://rss.dw.com/xml/rss-en-world", 0.88),
    RSSConnector("France24", "eu_editorial", "https://www.france24.com/en/rss", 0.88),
    RSSConnector("NPR", "us_public", "https://feeds.npr.org/1004/rss.xml", 0.87),
    RSSConnector("Al Jazeera", "global_south", "https://www.aljazeera.com/xml/rss/all.xml", 0.85),
    RSSConnector("CGTN", "china_state", "https://news.cgtn.com/news/rss/index.html", 0.75),
    RSSConnector("TASS", "russia_state", "https://tass.com/rss/v2.xml", 0.70),
    RSSConnector("Kyiv Independent", "ukraine_local", "https://kyivindependent.com/feed/", 0.83)
]

def build_hash(title, summary):
    raw = f"{title}|{summary}"
    return hashlib.sha256(raw.encode()).hexdigest()

def run_ingest(db: Session):
    fetched = 0
    inserted = 0
    duplicates = 0
    failures = []

    for connector in CONNECTORS:
        try:
            items = connector.fetch()

            for item in items:
                fetched += 1

                content_hash = build_hash(
                    item["title"],
                    item["summary"]
                )

                existing = db.query(Article).filter(
                    (Article.url == item["url"]) |
                    (Article.content_hash == content_hash)
                ).first()

                if existing:
                    duplicates += 1
                    continue

                article = Article(
                    id=str(uuid.uuid4()),
                    source=item["source"],
                    source_class=item["source_class"],
                    title=item["title"],
                    summary=item["summary"],
                    body=item["summary"],
                    url=item["url"],
                    trust_score=item["trust_score"],
                    content_hash=content_hash
                )

                db.add(article)
                inserted += 1

        except Exception as e:
            failures.append({
                "source": connector.name,
                "error": str(e)
            })

    db.commit()

    return {
        "fetched": fetched,
        "inserted": inserted,
        "duplicates": duplicates,
        "failures": failures
    }
