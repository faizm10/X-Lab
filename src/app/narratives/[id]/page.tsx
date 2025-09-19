import Link from "next/link";
import { narratives, articles } from "@/data/mock";
import { RadarChart } from "@/components/RadarChart";
import type { BiasScores } from "@/types";

export const dynamic = "force-dynamic";

function averageScores(ids: string[]): BiasScores {
  const picked = articles.filter((a) => ids.includes(a.id));
  const zero: BiasScores = { ideology: 0, factual: 0, framing: 0, emotion: 0, transparency: 0 };
  const acc: BiasScores = { ...zero };
  picked.forEach((a) => {
    for (const k of Object.keys(acc) as Array<keyof BiasScores>) {
      acc[k] += a.scores[k];
    }
  });
  const n = Math.max(1, picked.length);
  for (const k of Object.keys(acc) as Array<keyof BiasScores>) acc[k] = Math.round(acc[k] / n);
  return acc;
}

export default async function NarrativeDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const { items } = narratives;
  const narrative = items.find((n) => n.id === id);
  if (!narrative) {
    return (
      <main className="min-h-dvh bg-background text-foreground"><div className="mx-auto max-w-5xl px-6 md:px-10 py-12">Not found</div></main>
    );
  }
  const avg = averageScores(narrative.topArticles.map((a) => a.id));

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 py-12 md:py-16">
        <div className="flex items-center justify-between">
          <Link href="/narratives" className="text-sm hover:opacity-70">← Narratives</Link>
        </div>
        <header className="mt-6">
          <h1 className="text-3xl md:text-5xl font-semibold tracking-tight">{narrative.title}</h1>
          <p className="mt-3 text-foreground/70 max-w-2xl text-base">{narrative.summary}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {narrative.keywords.map((k) => (
              <span key={k} className="rounded-full border border-foreground/10 px-3 py-1 text-xs text-foreground/70">{k}</span>
            ))}
          </div>
        </header>

        <h2 className="mt-10 text-sm font-semibold tracking-tight">Bias over time</h2>
        <section className="mt-3 grid grid-cols-1 md:grid-cols-12 gap-8">
          <div className="md:col-span-8">
            <div className="rounded-2xl border border-foreground/10 p-4 bg-foreground/[.02] h-full min-h-[380px] lg:min-h-[420px] flex flex-col">
              <svg viewBox="0 0 800 260" width="100%" height="100%" preserveAspectRatio="none" className="flex-1">
                <defs>
                  <linearGradient id="lineFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.28" />
                    <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0" />
                  </linearGradient>
                </defs>
                {/* grid */}
                {Array.from({ length: 5 }).map((_, i) => (
                  <line key={i} x1={0} x2={800} y1={(i / 4) * 220 + 20} y2={(i / 4) * 220 + 20} stroke="currentColor" strokeOpacity={0.08} />
                ))}
                {(() => {
                  const values = narrative.sparkline;
                  const min = Math.min(...values);
                  const max = Math.max(...values);
                  const range = Math.max(1, max - min);
                  const points = values.map((v, i) => {
                    const x = 40 + (i / (values.length - 1)) * 720;
                    const y = 240 - ((v - min) / range) * 200;
                    return { x, y };
                  });
                  const path = points.map((p, i) => `${i === 0 ? "M" : "L"}${p.x},${p.y}`).join(" ");
                  const area = `${path} L ${points[points.length - 1].x},240 L 40,240 Z`;
                  return (
                    <g>
                      <path d={area} fill="url(#lineFill)" />
                      <path d={path} fill="none" stroke="#0ea5e9" strokeWidth={2} />
                    </g>
                  );
                })()}
              </svg>
            </div>
          </div>
          <aside className="md:col-span-4 self-stretch rounded-2xl border border-foreground/10 p-5 bg-foreground/[.02] h-full min-h-[380px] lg:min-h-[420px] flex flex-col items-center justify-center text-center gap-4">
            <h2 className="text-sm font-semibold tracking-tight">Average bias profile</h2>
            <div className="mt-1"><RadarChart scores={avg} /></div>
            <ul className="mt-1 w-full max-w-[280px] mx-auto space-y-2 text-sm">
              {(Object.keys(avg) as Array<keyof BiasScores>).map((k) => {
                const v = avg[k];
                return (
                  <li key={k} className="flex items-center gap-3">
                    <span className="capitalize w-28 text-foreground/70">{k}</span>
                    <div className="h-1.5 flex-1 rounded-full bg-foreground/10">
                      <div className="h-1.5 rounded-full bg-foreground/60" style={{ width: `${v}%` }} />
                    </div>
                    <span className="w-10 text-right tabular-nums">{v}</span>
                  </li>
                );
              })}
            </ul>
          </aside>
        </section>

        <section className="mt-12">
          <h3 className="text-sm font-semibold tracking-tight">Top articles</h3>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            {narrative.topArticles.map((a) => (
              <div key={a.id} className="rounded-2xl border border-foreground/10 p-5 bg-background/60 flex items-start justify-between">
                <div>
                  <Link href={`/articles/${a.id}`} className="font-medium hover:opacity-80 tracking-tight">{a.title}</Link>
                  <div className="text-xs text-foreground/60 mt-1">{a.outlet}</div>
                </div>
                <a href={a.url} target="_blank" rel="noopener noreferrer" className="text-xs rounded-full border border-foreground/15 px-3 py-1.5 hover:bg-foreground/5">Primary</a>
              </div>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}


