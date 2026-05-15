'use client';

import { useEffect, useMemo, useState } from 'react';
import Map, { Marker, Source, Layer } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';
import { Activity, Brain } from 'lucide-react';

type EventItem = {
  id: string;
  title: string;
  topic: string;
  article_count: number;
};

const GEO: Record<string, [number, number]> = {
  CHINA: [103, 35],
  RUSSIA: [105, 61],
  UKRAINE: [32, 49],
  USA: [-97, 38],
  ISRAEL: [35, 31],
  IRAN: [53, 32],
  INDIA: [78, 21],
  PAKISTAN: [69, 30],
  CUBA: [-79, 21],
  CONGO: [23, -2],
  TAIWAN: [121, 23],
  JAPAN: [138, 36],
};

function coords(topic: string): [number, number] {
  for (const key of Object.keys(GEO)) {
    if (topic.includes(key)) return GEO[key];
  }
  return [Math.random() * 360 - 180, Math.random() * 140 - 70];
}

function Panel({ title, children }: any) {
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-5">
      <div className="text-sm uppercase tracking-[0.2em] text-cyan-300 mb-4">
        {title}
      </div>
      {children}
    </div>
  );
}

export default function Home() {
  const [events, setEvents] = useState<EventItem[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/events')
      .then((r) => r.json())
      .then(setEvents);
  }, []);

  const geojson = useMemo(() => ({
    type: 'FeatureCollection',
    features: events.slice(0, 20).map((e) => {
      const [lng, lat] = coords(e.topic);

      return {
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [lng, lat],
        },
        properties: {
          title: e.title,
        },
      };
    }),
  }), [events]);

  return (
    <main className="min-h-screen bg-black text-white px-6 py-5">
      <div className="max-w-[1900px] mx-auto space-y-6">

        <header className="flex justify-between items-end">
          <div>
            <h1 className="text-6xl font-bold tracking-tight">DialecticOS</h1>
            <p className="text-white/50 text-lg mt-2">
              Strategic Intelligence Command Center
            </p>
          </div>

          <div className="text-sm text-cyan-300 tracking-[0.25em] animate-pulse">
            LIVE SIGNAL ACTIVE
          </div>
        </header>

        <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 px-4 py-2 text-sm text-cyan-300 overflow-hidden whitespace-nowrap">
          CHINA / TAIWAN DIPLOMATIC SIGNAL • ISRAEL CEASEFIRE UPDATE • IRAN NUCLEAR POSTURE • CONGO HEALTH EVENT
        </div>

        <Panel title="Global Intelligence Surface">
          <div className="h-[850px] rounded-xl overflow-hidden">
            <Map
              initialViewState={{
                longitude: 15,
                latitude: 20,
                zoom: 1.35,
              }}
              mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
            >
              <Source id="events" type="geojson" data={geojson as any}>
                <Layer
                  id="event-points"
                  type="circle"
                  paint={{
                    'circle-radius': 8,
                    'circle-color': '#00ffff',
                    'circle-opacity': 0.8,
                    'circle-blur': 0.3,
                  }}
                />
              </Source>

              {events.slice(0, 20).map((event) => {
                const [lng, lat] = coords(event.topic);

                return (
                  <Marker key={event.id} longitude={lng} latitude={lat}>
                    <div className="h-3 w-3 rounded-full bg-cyan-400 shadow-[0_0_18px_#00ffff]" />
                  </Marker>
                );
              })}
            </Map>
          </div>
        </Panel>

        <div className="grid grid-cols-2 gap-6">
          <Panel title="Live Events">
            <div className="space-y-3 max-h-[420px] overflow-y-auto">
              {events.slice(0, 12).map((event) => (
                <div
                  key={event.id}
                  className="rounded-xl border border-white/10 p-4 hover:border-cyan-500/40 transition"
                >
                  <div className="flex items-start gap-3">
                    <Activity size={16} className="text-cyan-400 mt-1" />
                    <div>
                      <div className="font-medium">{event.title}</div>

                      <div className="flex gap-2 mt-3 flex-wrap">
                        <span className="text-xs px-2 py-1 rounded bg-cyan-500/10 text-cyan-300">
                          {event.topic.split('-')[0]}
                        </span>

                        <span className="text-xs px-2 py-1 rounded bg-white/10 text-white/70">
                          {event.article_count} sources
                        </span>

                        <span className="text-xs px-2 py-1 rounded bg-red-500/10 text-red-300">
                          HIGH
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </Panel>

          <Panel title="AI Strategic Analysis">
            <div className="space-y-5">
              <div className="rounded-xl border border-white/10 p-5">
                <div className="flex items-center gap-3 mb-3">
                  <Brain size={18} className="text-cyan-400" />
                  <div className="font-medium">Consensus Engine</div>
                </div>
                <p className="text-white/60">
                  Detecting narrative convergence.
                </p>
              </div>

              <div className="rounded-xl border border-white/10 p-5">
                <div className="font-medium mb-2">Divergence Detection</div>
                <p className="text-white/60">
                  Identifying asymmetric geopolitical reporting.
                </p>
              </div>

              <div className="rounded-xl border border-white/10 p-5">
                <div className="font-medium mb-2">Executive Briefing</div>
                <p className="text-white/60">
                  AI synthesis pending backend wiring.
                </p>
              </div>
            </div>
          </Panel>
        </div>
      </div>
    </main>
  );
}
