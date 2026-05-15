import re
import uuid
from collections import defaultdict

import spacy
from sqlalchemy.orm import Session

from app.db.models.article import Article
from app.db.models.event import Event

nlp = spacy.load("en_core_web_sm")

NOISE_PATTERNS = [
    r"^LIVE:",
    r"^Video:",
    r"Premier League",
    r"World Cup",
    r"Messi",
    r"Auto Show"
]

VERB_MAP = {
    "attack": "ATTACK",
    "strike": "ATTACK",
    "bomb": "ATTACK",
    "drone": "ATTACK",
    "sanction": "SANCTIONS",
    "trade": "TRADE",
    "ceasefire": "CEASEFIRE",
    "talks": "DIPLOMACY",
    "meeting": "DIPLOMACY",
    "summit": "DIPLOMACY",
    "kills": "CASUALTY",
    "detention": "LEGAL",
    "court": "LEGAL"
}

COUNTRY_ALIASES = {
    "kiev": "UKRAINE",
    "ukraine": "UKRAINE",
    "russia": "RUSSIA",
    "moscow": "RUSSIA",
    "kremlin": "RUSSIA",
    "china": "CHINA",
    "beijing": "CHINA",
    "usa": "USA",
    "u.s.": "USA",
    "united states": "USA",
    "israel": "ISRAEL",
    "iran": "IRAN",
    "pakistan": "PAKISTAN",
    "india": "INDIA"
}

def is_noise(title):
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, title, re.IGNORECASE):
            return True
    return False

def normalize_actor(name):
    key = name.lower().strip()
    return COUNTRY_ALIASES.get(key, name.upper())

def detect_action(text):
    t = text.lower()
    for k, v in VERB_MAP.items():
        if k in t:
            return v
    return "GENERAL"

def fingerprint(article):
    doc = nlp(article.title)

    actors = []
    places = []

    for ent in doc.ents:
        if ent.label_ in ("GPE", "ORG"):
            norm = normalize_actor(ent.text)
            if norm not in actors:
                actors.append(norm)

        if ent.label_ == "LOC":
            loc = ent.text.upper()
            if loc not in places:
                places.append(loc)

    action = detect_action(article.title)

    actor_part = "-".join(sorted(actors[:2])) if actors else "UNKNOWN"
    place_part = "-".join(sorted(places[:1])) if places else "GLOBAL"

    return f"{actor_part}-{place_part}-{action}"

def cluster_articles(db: Session):
    articles = db.query(Article).all()

    filtered = [
        a for a in articles
        if not is_noise(a.title)
    ]

    groups = defaultdict(list)

    for article in filtered:
        fp = fingerprint(article)
        groups[fp].append(article)

    db.query(Event).delete()

    for fp, items in groups.items():
        evt = Event(
            id=str(uuid.uuid4()),
            title=items[0].title,
            topic=fp,
            confidence=0.92,
            article_count=len(items)
        )
        db.add(evt)

    db.commit()

    return {
        "articles": len(filtered),
        "events": len(groups)
    }
