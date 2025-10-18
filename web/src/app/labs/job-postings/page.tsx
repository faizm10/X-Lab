import Link from "next/link";
import { labs } from "../../../data/mock";

export const dynamic = "force-dynamic";

export default async function RefereeDecisionBias() {
  const { items } = labs;
  const lab = items.find((n) => n.id === "job-postings");
  
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
          <p className="mt-2 text-sm text-foreground/60">Under Construction</p>
          
          <div className="mt-4 flex flex-wrap gap-2">
            {lab.keywords.map((k) => (
              <span key={k} className="rounded-full border border-foreground/10 px-3 py-1 text-xs text-foreground/70">{k}</span>
            ))}
          </div>
        </header>

        {/* GO Transit Specific Layout */}
        <section className="mt-12">
            <h2 className="text-4xl font-semibold tracking-tight mb-8">Under Construction</h2>
        </section>
      </div>
    </main>
  );
}
