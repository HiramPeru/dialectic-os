import feedparser
from bs4 import BeautifulSoup

class RSSConnector:
    def __init__(self, name, source_class, url, trust_score=0.8):
        self.name = name
        self.source_class = source_class
        self.url = url
        self.trust_score = trust_score

    def clean(self, text):
        if not text:
            return ""
        return BeautifulSoup(text, "html.parser").get_text(" ", strip=True)

    def fetch(self):
        feed = feedparser.parse(self.url)
        rows = []

        for entry in feed.entries[:20]:
            rows.append({
                "source": self.name,
                "source_class": self.source_class,
                "title": self.clean(getattr(entry, "title", "")),
                "summary": self.clean(getattr(entry, "summary", "")),
                "url": getattr(entry, "link", ""),
                "published": getattr(entry, "published", None),
                "trust_score": self.trust_score
            })

        return rows
