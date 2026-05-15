from app.services.ai.ollama_client import ask_gemma

def consensus_from_articles(articles):
    joined = "\n\n".join([
        f"SOURCE: {a.source}\nTITLE: {a.title}\nSUMMARY: {a.summary}"
        for a in articles[:8]
    ])

    prompt = f"""
You are a geopolitical intelligence analyst.

Given multiple news reports about the same event:

1. Extract only facts consistently supported.
2. Ignore propaganda language.
3. Produce concise analyst-grade summary.

ARTICLES:
{joined}

OUTPUT:
Consensus facts:
"""

    return ask_gemma(prompt)
