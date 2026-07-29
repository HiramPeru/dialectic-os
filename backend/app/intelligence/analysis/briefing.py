from app.intelligence.providers import generate_text

def executive_briefing(articles):
    joined = "\n\n".join([
        f"{a.source}: {a.title}"
        for a in articles[:10]
    ])

    prompt = f"""
Create executive geopolitical briefing.

Include:

- what happened
- who is involved
- immediate risks
- what deserves analyst attention

INPUT:
{joined}
"""

    return generate_text(
        prompt,
        system_prompt=(
            "You produce concise strategic briefings from supplied evidence. "
            "Mark uncertainty explicitly and do not add unsupported facts."
        ),
    )
