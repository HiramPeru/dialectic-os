"use client";

import { useEffect, useMemo, useState } from "react";
import { Search, Globe, Activity, ShieldAlert, Newspaper, ExternalLink } from "lucide-react";

type Event = {
  id: string;
  title: string;
  topic: string;
  article_count: number;
};

type Article = {
  id: string;
  source: string;
  title: string;
  url: string;
};

const API = "http://127.0.0.1:8000";

export default function DialecticDashboard() {
  const [events, setEvents] = useState<Event[]>([]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [selected, setSelected] = useState<Event | null>(null);
  const [query, setQuery] = useState("");

  async function load() {
    await fetch(`${API}/events/cluster`, { method: "POST" });

    const [ev, ar] = await Promise.all([
      fetch(`${API}/events`).then(r => r.json()),
      fetch(`${API}/articles`).then(r => r.json())
    ]);

    setEvents(ev);
    setArticles(ar);

    if (ev.length) setSelected(ev[0]);
  }

  useEffect(() => {
    load();
  }, []);

  const filteredEvents = useMemo(() => {
    return events
      .filter(e => e.title.toLowerCase().includes(query.toLowerCase()))
      .sort((a, b) => b.article_count - a.article_count);
  }, [events, query]);

  const related = useMemo(() => {
    if (!selected) return [];
    const token = selected.title.split(" ")[0].toLowerCase();
    return articles.filter(a =>
      a.title.toLowerCase().includes(token)
    ).slice(0, 12);
  }, [selected, articles]);

  const totalArticles = events.reduce((s, e) => s + e.article_count, 0);

  return (
    <main className="min-h-screen bg-[#05070B] text-zinc-100 p-4">
      <div className="grid grid-cols-12 gap-4 h-screen">
        <div className="col-span-12 border border-zinc-800 rounded-3xl bg-[#0A0E14] px-6 py-4 flex items-center justify-between">
          <div>
            <div className="text-2xl font-bold">DIALECTIC INTELLIGENCE</div>
            <div className="text-xs text-zinc-400 uppercase tracking-[0.25em]">
              Global Narrative Divergence Console
            </div>
          </div>

          <div className="grid grid-cols-4 gap-4 w-[60%]">
            <Metric icon={<Newspaper size={16} />} label="Events" value={events.length} />
            <Metric icon={<Globe size={16} />} label="Articles" value={totalArticles} />
            <Metric icon={<Activity size={16} />} label="Density" value={events.length ? (totalArticles / events.length).toFixed(2) : "0"} />
            <Metric icon={<ShieldAlert size={16} />} label="Risk" value="MED" />
          </div>
        </div>

        <div className="col-span-3 border border-zinc-800 rounded-3xl bg-[#0A0E14] p-4 overflow-y-auto">
          <div className="flex items-center gap-2 border border-zinc-700 rounded-2xl px-3 py-2 mb-4">
            <Search size={16} />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search events"
              className="bg-transparent outline-none w-full"
            />
          </div>

          <button
            onClick={load}
            className="mb-4 rounded-2xl px-4 py-2 bg-cyan-700 hover:bg-cyan-600 w-full"
          >
            Refresh Intelligence
          </button>

          <div className="space-y-3">
            {filteredEvents.map((event) => (
              <button
                key={event.id}
                onClick={() => setSelected(event)}
                className="w-full text-left rounded-2xl p-4 border border-zinc-800 bg-[#0F141C] hover:border-cyan-500"
              >
                <div className="text-sm font-semibold">{event.title}</div>
                <div className="mt-2 text-xs text-zinc-400">
                  {event.article_count} sources
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="col-span-5 border border-zinc-800 rounded-3xl bg-[#0A0E14] p-6">
          {selected && (
            <>
              <div className="text-xs uppercase tracking-[0.3em] text-cyan-400 mb-3">
                Event Detail
              </div>

              <h2 className="text-3xl font-bold mb-6">{selected.title}</h2>

              <div className="grid grid-cols-3 gap-3">
                <Mini label="Topic" value={selected.topic} />
                <Mini label="Sources" value={selected.article_count} />
                <Mini label="Confidence" value="92%" />
              </div>
            </>
          )}
        </div>

        <div className="col-span-4 border border-zinc-800 rounded-3xl bg-[#0A0E14] p-6 overflow-y-auto">
          <div className="text-xs uppercase tracking-[0.3em] text-amber-400 mb-4">
            Narrative Sources
          </div>

          <div className="space-y-3">
            {related.map((article) => (
              <a
                key={article.id}
                href={article.url}
                target="_blank"
                rel="noreferrer"
                className="block border border-zinc-800 rounded-2xl p-4 bg-[#0F141C] hover:border-amber-500"
              >
                <div className="flex justify-between mb-2">
                  <span className="text-xs px-2 py-1 rounded-full bg-zinc-800">
                    {article.source}
                  </span>
                  <ExternalLink size={14} />
                </div>

                <div className="text-sm font-medium">
                  {article.title}
                </div>
              </a>
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}

function Metric({ icon, label, value }: any) {
  return (
    <div className="border border-zinc-800 rounded-2xl p-3 bg-[#0F141C]">
      <div className="flex items-center gap-2 text-xs text-zinc-400 uppercase">
        {icon}{label}
      </div>
      <div className="text-2xl font-bold mt-2">{value}</div>
    </div>
  );
}

function Mini({ label, value }: any) {
  return (
    <div className="border border-zinc-800 rounded-2xl p-3 bg-[#0F141C]">
      <div className="text-xs text-zinc-400 uppercase">{label}</div>
      <div className="mt-2 text-sm font-semibold break-words">{value}</div>
    </div>
  );
}
