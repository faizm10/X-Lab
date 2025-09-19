import Link from "next/link";
import { narratives } from "@/data/mock";
import { NarrativeCard } from "@/components/NarrativeCard";

export const dynamic = "force-dynamic";

export default function Home() {
  const { items } = narratives;
  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 min-h-dvh flex flex-col">
        <nav className="flex items-center justify-end py-6">
          <div className="hidden md:flex items-center gap-6 text-sm">
            <Link href="narratives" className="hover:opacity-70 transition-opacity">Narratives</Link>
            <a
              href="https://github.com/emmaashi/the-bias-lab"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center rounded-full bg-foreground text-background px-4 py-2 text-sm font-medium hover:opacity-90"
            >
              View Code
            </a>
          </div>
        </nav>

        <section className="grid grid-cols-1 md:grid-cols-8 items-center gap-8 py-16 md:py-20">
          <div className="md:col-span-5">
            <h1 className="text-4xl md:text-6xl font-semibold tracking-tight leading-[1.05]">
              Truth has dimensions. 
              Explore them.
            </h1>
            <p className="mt-6 text-base md:text-lg text-foreground/70 max-w-3xl">
            We score every news article across five dimensions—ideology, facts, framing, emotion, and transparency—then cluster them to reveal how narratives evolve across outlets. 
             </p>
          </div>
        </section>

        <section id="trending-narratives">
          <div className="mb-6 flex items-end justify-between">
            <h2 className="text-xl font-semibold tracking-tight">Trending narratives</h2>
            <Link href="/narratives" className="text-sm hover:opacity-70">View all</Link>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {items.slice(0, 3).map((n) => (
              <NarrativeCard key={n.id} narrative={n} />
            ))}
          </div>
        </section>
        <footer className="mt-auto py-10 border-t border-foreground/10 text-sm text-foreground/60">
          <div className="flex items-center justify-between">
            <span>© {new Date().getFullYear()} Emma Shi</span>
          </div>
        </footer>
      </div>
    </main>
  );
}
