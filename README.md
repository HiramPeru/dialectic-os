# Dialectic OS — Early Prototype (Archived)

> **Status: Archived / Superseded.** This repository is the original May 2026
> proof-of-concept for what became **[DialecticDashboard](https://github.com/HiramPeru/DialecticDashboard)**,
> the current disciplined rebuild of DialecticOS. This code is not maintained
> and should not be deployed. It is preserved as a reference implementation
> for the analysis pipeline that DialecticDashboard has not yet reimplemented.

## What this was

A working prototype of a multi-source geopolitical narrative analysis engine:

- **Ingestion**: RSS connectors for 10 news sources spanning the editorial
  spectrum (Reuters/AP as `fact_core`, BBC/DW/France24 as Western editorial,
  CGTN/TASS as state media, Al Jazeera as Global South, Kyiv Independent as
  local), each with a `trust_score` and `source_class`. Deduplication via
  content hash.
- **Clustering**: NER-based (spaCy) fingerprinting of articles by
  actor/place/action into discrete events.
- **Analysis** (via local Ollama/Gemma):
  - `consensus_from_articles` — facts consistently supported across sources.
  - `divergence_from_articles` — conflicting claims, blame attribution,
    framing and terminology differences, omitted context.
  - `executive_briefing` — analyst-style summary of what happened, who's
    involved, and what deserves attention.

## Why it was superseded

This prototype validated the product idea but not the production design:

- Local LLM (Ollama) instead of the evaluated remote-provider strategy
  (NVIDIA NIM primary, DeepSeek fallback) formalized in DialecticDashboard's
  ADR-001.
- No formal ontology, data dictionary, or documentary provenance model —
  DialecticDashboard's ontology v1.1 defines this rigorously.
- No test suite, no API contract, no migration discipline.

## Relationship to DialecticDashboard

DialecticDashboard does not yet reimplement this analysis pipeline (it is
currently frontend + schema + API contract only). The consensus/divergence/
clustering logic here is a useful reference for that future implementation,
rewritten against the accepted ontology and remote LLM providers — not code
to port as-is.

## Running (historical reference only)

```bash
docker compose up -d   # postgres + redis
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload
cd ../apps/web && npm install && npm run dev
```

No `.env` secrets are required beyond local Postgres defaults; this was
never connected to production credentials or real user data.
