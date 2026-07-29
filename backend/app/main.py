from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import health, events, ingest, articles, intelligence
from app.core.config import settings

app = FastAPI(title="DialecticOS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(events.router, prefix="/events")
app.include_router(ingest.router, prefix="/ingest")
app.include_router(articles.router, prefix="/articles")

app.include_router(intelligence.router, prefix='/intelligence')
