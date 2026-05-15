from app.intelligence.providers.ollama import ask_gemma

def divergence_from_articles(articles):
    joined = "\n\n".join([
        f"SOURCE: {a.source}\nTITLE: {a.title}\nSUMMARY: {a.summary}"
        for a in articles[:8]
    ])

    prompt = f"""
You are an intelligence analyst.

Compare these reports.

Identify:

- conflicting claims
- blame attribution differences
- emotional framing differences
- terminology differences
- omitted context

ARTICLES:
{joined}

OUTPUT:
Narrative divergence analysis:
"""

    return ask_gemma(prompt)
