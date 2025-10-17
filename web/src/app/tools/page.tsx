import Link from "next/link";
import { tools } from "../../data/mock";

export const dynamic = "force-dynamic";

export default function ToolsPage() {
  const { items } = tools;

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 py-16 md:py-24">
        <div className="flex items-end justify-between gap-6">
          <div>
            <h1 className="text-3xl md:text-4xl font-semibold tracking-tight">Tools & Utilities</h1>
            <p className="mt-2 text-foreground/60 text-sm">Practical tools and automation projects.</p>
          </div>
          <Link href="/" className="text-sm hover:opacity-70">Home</Link>
        </div>

        <section className="mt-10">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {items.map((tool) => (
              <Link 
                key={tool.id} 
                href={`/tools/${tool.id}`}
                className="group rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6 hover:bg-foreground/[0.04] transition-all"
              >
                <div className="flex items-start justify-between">
                  <h2 className="text-xl font-semibold group-hover:text-foreground/80 transition-colors">
                    {tool.title}
                  </h2>
                  <svg 
                    className="w-5 h-5 text-foreground/40 group-hover:translate-x-1 transition-transform" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <p className="mt-3 text-sm text-foreground/60 line-clamp-2">
                  {tool.summary}
                </p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {tool.keywords.slice(0, 3).map((k) => (
                    <span 
                      key={k} 
                      className="rounded-full border border-foreground/10 px-2.5 py-0.5 text-xs text-foreground/60"
                    >
                      {k}
                    </span>
                  ))}
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

