from sqlalchemy import Column, String, Text, Numeric, Integer
from app.core.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    title = Column(Text, nullable=False)
    topic = Column(String)
    confidence = Column(Numeric)
    article_count = Column(Integer)
