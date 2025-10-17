import Link from "next/link";
import { labs, tools } from "../data/mock";
import { NarrativeCard } from "../components/NarrativeCard";

export const dynamic = "force-dynamic";

export default function Home() {
  const { items: labItems } = labs;
  const { items: toolItems } = tools;
  
  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 min-h-dvh flex flex-col">
        <nav className="flex items-center justify-end py-6">
          <div className="hidden md:flex items-center gap-6 text-sm">
            <Link href="labs" className="hover:opacity-70 transition-opacity">Labs</Link>
            <Link href="tools" className="hover:opacity-70 transition-opacity">Tools</Link>
            <a
              href="https://github.com/faizm10/faiz-lab"
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
              Faiz Labs — personal backend experiments & metrics.
            </h1>
            <p className="mt-6 text-base md:text-lg text-foreground/70 max-w-3xl">
            A tidy place where I test ideas, log results, and make small bets with data.
             </p>
          </div>
        </section>

        <section id="trending-labs" className="space-y-12">
          <div>
            <div className="mb-6 flex items-end justify-between">
              <h2 className="text-xl font-semibold tracking-tight">Active Labs</h2>
              <Link href="/labs" className="text-sm hover:opacity-70">View all</Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {labItems.slice(0, 3).map((n) => (
                <NarrativeCard key={n.id} narrative={n} baseUrl="/labs" />
              ))}
            </div>
          </div>

          <div>
            <div className="mb-6 flex items-end justify-between">
              <h2 className="text-xl font-semibold tracking-tight">Tools & Utilities</h2>
              <Link href="/tools" className="text-sm hover:opacity-70">View all</Link>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {toolItems.slice(0, 3).map((n) => (
                <NarrativeCard key={n.id} narrative={n} baseUrl="/tools" />
              ))}
            </div>
          </div>
        </section>
        <footer className="mt-auto py-10 border-t border-foreground/10 text-sm text-foreground/60">
          <div className="flex items-center justify-between">
            <span>© {new Date().getFullYear()} Faiz Mustansar</span>
          </div>
        </footer>
      </div>
    </main>
  );
}
