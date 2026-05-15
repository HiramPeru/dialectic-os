from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import health, events, ingest, articles, intelligence

app = FastAPI(title="Dialectic Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(events.router, prefix="/events")
app.include_router(ingest.router, prefix="/ingest")
app.include_router(articles.router, prefix="/articles")

app.include_router(intelligence.router, prefix='/intelligence')
