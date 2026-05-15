from app.services.ai.ollama_client import ask_gemma

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

    return ask_gemma(prompt)
