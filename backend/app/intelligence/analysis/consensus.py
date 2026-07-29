from app.intelligence.providers import generate_text

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

    return generate_text(
        prompt,
        system_prompt=(
            "You identify only claims supported by the supplied evidence. "
            "Separate verified facts from uncertainty and never invent sources."
        ),
    )
