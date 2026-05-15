from sqlalchemy import Column, String, Text, DateTime, Numeric
from app.core.db import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    source_class = Column(String)
    title = Column(Text, nullable=False)
    summary = Column(Text)
    body = Column(Text)
    url = Column(Text, unique=True, nullable=False)
    published_at = Column(DateTime)
    trust_score = Column(Numeric)
    content_hash = Column(String, unique=True)
