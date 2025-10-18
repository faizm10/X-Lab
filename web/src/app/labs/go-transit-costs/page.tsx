import Link from "next/link";
import { labs } from "../../../data/mock";
import { RadarChart } from "../../../components/RadarChart";
import type { BiasScores } from "../../../types";

export const dynamic = "force-dynamic";

// Placeholder performance metrics for the lab
const placeholderMetrics: BiasScores = {
  ideology: 50,
  factual: 85,
  framing: 60,
  emotion: 45,
  transparency: 80,
};

export default async function GoTransitCostsLab() {
  const { items } = labs;
  const lab = items.find((n) => n.id === "go-transit-costs");
  
  if (!lab) {
    return (
      <main className="min-h-dvh bg-background text-foreground">
        <div className="mx-auto max-w-5xl px-6 md:px-10 py-12">Lab not found</div>
      </main>
    );
  }
  
  // Use placeholder metrics instead of calculating from articles

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 py-12 md:py-16">
        <div className="flex items-center justify-between">
          <Link href="/labs" className="text-sm hover:opacity-70">← Labs</Link>
        </div>
        
        <header className="mt-6">
          <h1 className="text-3xl md:text-5xl font-semibold tracking-tight">{lab.title}</h1>
          <p className="mt-3 text-foreground/70 max-w-2xl text-base">{lab.summary}</p>
          <p className="mt-2 text-sm text-foreground/60">I commute a lot. This lab asks: what&apos;s the best tradeoff between money and time?</p>
          
          <div className="mt-4 flex flex-wrap gap-2">
            {lab.keywords.map((k) => (
              <span key={k} className="rounded-full border border-foreground/10 px-3 py-1 text-xs text-foreground/70">{k}</span>
            ))}
          </div>
        </header>

        {/* GO Transit Specific Layout */}
        <section className="mt-12">
          <h2 className="text-lg font-semibold tracking-tight mb-8">Cost Analysis Dashboard</h2>
          
          {/* Metric Cards Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            <div className="rounded-2xl border border-foreground/10 p-6 bg-foreground/[.02]">
              <h3 className="text-sm font-medium text-foreground/70">Avg Cost (Train+Bus)</h3>
              <p className="text-2xl font-semibold mt-2">$8.50</p>
              <p className="text-xs text-foreground/50 mt-2">per trip</p>
            </div>
            <div className="rounded-2xl border border-foreground/10 p-6 bg-foreground/[.02]">
              <h3 className="text-sm font-medium text-foreground/70">Avg Cost (Bus+Bus)</h3>
              <p className="text-2xl font-semibold mt-2">$7.25</p>
              <p className="text-xs text-foreground/50 mt-2">per trip</p>
            </div>
            <div className="rounded-2xl border border-foreground/10 p-6 bg-foreground/[.02]">
              <h3 className="text-sm font-medium text-foreground/70">Time Saved</h3>
              <p className="text-2xl font-semibold mt-2 text-green-600">-14.7 min</p>
              <p className="text-xs text-foreground/50 mt-2">train+bus vs bus+bus</p>
            </div>
            <div className="rounded-2xl border border-foreground/10 p-6 bg-foreground/[.02]">
              <h3 className="text-sm font-medium text-foreground/70">Cost per Minute</h3>
              <p className="text-2xl font-semibold mt-2">$0.11</p>
              <p className="text-xs text-foreground/50 mt-2">train+bus efficiency</p>
            </div>
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            <div className="lg:col-span-2">
              <h3 className="text-sm font-semibold tracking-tight mb-6">Activity over time</h3>
              <div className="rounded-2xl border border-foreground/10 p-6 bg-foreground/[.02] h-full min-h-[300px] flex flex-col">
                <svg viewBox="0 0 800 200" width="100%" height="100%" preserveAspectRatio="none" className="flex-1">
                  <defs>
                    <linearGradient id="lineFill" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#0ea5e9" stopOpacity="0.28" />
                      <stop offset="100%" stopColor="#0ea5e9" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  {/* grid */}
                  {Array.from({ length: 5 }).map((_, i) => (
                    <line key={i} x1={0} x2={800} y1={(i / 4) * 160 + 20} y2={(i / 4) * 160 + 20} stroke="currentColor" strokeOpacity={0.08} />
                  ))}
                  {(() => {
                    const values = lab.sparkline;
                    const min = Math.min(...values);
                    const max = Math.max(...values);
                    const range = Math.max(1, max - min);
                    const points = values.map((v, i) => {
                      const x = 40 + (i / (values.length - 1)) * 720;
                      const y = 180 - ((v - min) / range) * 140;
                      return { x, y };
                    });
                    const path = points.map((p, i) => `${i === 0 ? "M" : "L"}${p.x},${p.y}`).join(" ");
                    const area = `${path} L ${points[points.length - 1].x},180 L 40,180 Z`;
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
            
            <div className="lg:col-span-1">
              <h3 className="text-sm font-semibold tracking-tight mb-6">Performance Metrics</h3>
              <div className="rounded-2xl border border-foreground/10 p-6 bg-foreground/[.02] h-full min-h-[300px] flex flex-col items-center justify-center text-center gap-4">
                <div className="mt-1"><RadarChart scores={placeholderMetrics} /></div>
                <ul className="mt-1 w-full max-w-[280px] mx-auto space-y-2 text-sm">
                  {(Object.keys(placeholderMetrics) as Array<keyof BiasScores>).map((k) => {
                    const v = placeholderMetrics[k];
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
              </div>
            </div>
          </div>

          {/* Scenario Analysis */}
          <div className="rounded-2xl border border-foreground/10 p-8 bg-foreground/[.02] mb-12">
            <h3 className="text-sm font-semibold tracking-tight mb-6">Scenario Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h4 className="text-sm font-medium text-foreground/70 mb-3">If every trip were bus+bus:</h4>
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span>Money saved:</span>
                    <span className="font-medium text-green-600">+$12.00</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Time lost:</span>
                    <span className="font-medium text-red-600">+180 minutes</span>
                  </div>
                </div>
              </div>
              <div>
                <h4 className="text-sm font-medium text-foreground/70 mb-3">Value of Time:</h4>
                <div className="text-2xl font-semibold">12.3 min/$</div>
                <p className="text-xs text-foreground/50 mt-2">How many minutes you save per dollar spent</p>
              </div>
            </div>
          </div>

          {/* Related Projects */}
          <div>
            <h3 className="text-sm font-semibold tracking-tight mb-6">Related Projects</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {lab.topArticles.map((project) => (
                <div key={project.id} className="rounded-2xl border border-foreground/10 p-6 bg-background/60 flex items-start justify-between">
                  <div>
                    <div className="font-medium hover:opacity-80 tracking-tight">{project.title}</div>
                    <div className="text-xs text-foreground/60 mt-2">{project.outlet}</div>
                  </div>
                  <div className="text-xs rounded-full border border-foreground/15 px-3 py-1.5 hover:bg-foreground/5">
                    View
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
