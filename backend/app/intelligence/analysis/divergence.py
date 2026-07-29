from app.intelligence.providers import generate_text

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

    return generate_text(
        prompt,
        system_prompt=(
            "You compare narratives without assuming that any source is neutral. "
            "Tie every conclusion to the supplied reports."
        ),
    )
