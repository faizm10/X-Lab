import Link from "next/link";
import { narratives } from "@/data/mock";
import { NarrativeCard } from "@/components/NarrativeCard";

export const dynamic = "force-dynamic";

export default function NarrativesPage() {
  const { items } = narratives;

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 py-16 md:py-24">
        <div className="flex items-end justify-between gap-6">
          <div>
            <h1 className="text-3xl md:text-4xl font-semibold tracking-tight">Trending narratives</h1>
            <p className="mt-2 text-foreground/60 text-sm">Clusters reflect intensity and shared framing.</p>
          </div>
          <Link href="/" className="text-sm hover:opacity-70">Home</Link>
        </div>

        <section className="mt-10">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {items.map((n) => (
              <NarrativeCard key={n.id} narrative={n} />
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}


