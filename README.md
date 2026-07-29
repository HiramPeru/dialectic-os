# DialecticOS

Personal evidence and narrative intelligence workspace. The system ingests
multiple sources, groups related reporting and produces consensus, divergence
and briefing analyses while preserving the underlying source records.

## Architecture

- `apps/web`: Next.js interface, deployable independently to Vercel.
- `backend`: FastAPI ingestion and intelligence API.
- PostgreSQL: articles, events and later evidence/claim relationships.
- Redis: reserved for asynchronous work and caching.
- Remote LLM: NVIDIA NIM by default; direct DeepSeek API as an alternative.

No local LLM runtime is required.

## Model provider

Copy `.env.example` to `.env`, then configure one provider:

```dotenv
LLM_PROVIDER=nvidia
NVIDIA_API_KEY=nvapi-...
```

The default NVIDIA model is `deepseek-ai/deepseek-v4-pro`. To use DeepSeek
directly:

```dotenv
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-v4-flash
DEEPSEEK_API_KEY=...
```

Both providers use the same OpenAI-compatible client. API keys remain only in
the backend environment and are never exposed to the browser.

## Local backend

```bash
docker compose up -d
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

Health and provider configuration are visible at
`http://127.0.0.1:8000/health`. The endpoint reports whether the selected
provider has a key, but never returns the key.

## Local web interface

```bash
cd apps/web
cp .env.example .env.local
npm ci
npm run dev
```

## Vercel

Import this repository as a Vercel project and configure:

1. Root Directory: `apps/web`
2. Framework Preset: Next.js
3. Environment variable:
   `NEXT_PUBLIC_API_URL=https://<public-backend-host>`

On the backend, add the Vercel production and preview origins to
`CORS_ORIGINS`, separated by commas. The FastAPI service and its API keys
remain outside the Vercel browser bundle.

## Tests

```bash
cd backend
python -m unittest discover -s tests -v
```
