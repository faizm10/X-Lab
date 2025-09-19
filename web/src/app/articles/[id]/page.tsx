import Link from "next/link";
import { articles } from "../../../data/mock";
import { RadarChart } from "../../../components/RadarChart";
import { Highlights } from "../../../components/Highlights";
import type { BiasScores } from "../../../types";

export const dynamic = "force-dynamic";

export default async function ArticlePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const article = articles.find(a => a.id === id);
  
  if (!article) {
    return (
      <main className="min-h-dvh bg-background text-foreground">
        <div className="mx-auto max-w-5xl px-6 md:px-10 py-12 md:py-16">
          <h1 className="text-2xl font-semibold">Article not found</h1>
          <Link href="/narratives" className="text-sm hover:opacity-70 mt-4 inline-block">← Back to Narratives</Link>
        </div>
      </main>
    );
  }
  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-5xl px-6 md:px-10 py-12 md:py-16">
        <div className="flex items-center justify-between gap-6">
          <Link href="/narratives" className="text-sm hover:opacity-70">← Narratives</Link>
          <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-sm rounded-full border border-foreground/15 px-3 py-1.5 hover:bg-foreground/5">Primary source</a>
        </div>

        <header className="mt-8">
          <div className="text-xs text-foreground/60">{article.outlet} • {new Date(article.publishedAt).toLocaleString()}</div>
          <h1 className="mt-2 text-3xl md:text-4xl font-semibold tracking-tight">{article.title}</h1>
          {article.author && <p className="mt-1 text-sm text-foreground/60">By {article.author}</p>}
        </header>

        <section className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-2">
            <Highlights text={article.content} spans={article.highlights} />
          </div>
          <aside className="md:col-span-1 rounded-2xl border border-foreground/10 p-4">
            <h2 className="text-sm font-semibold tracking-tight">Bias profile</h2>
            <div className="mt-4">
              <RadarChart scores={article.scores} />
            </div>
            <ul className="mt-4 space-y-2 text-sm">
              {(Object.keys(article.scores) as Array<keyof BiasScores>).map((k) => (
                <li key={k} className="flex justify-between"><span className="capitalize">{k}</span><span>{article.scores[k]}</span></li>
              ))}
            </ul>
            {article.timeline && (
              <div className="mt-6">
                <h3 className="text-xs text-foreground/60">Bias over time</h3>
                <div className="mt-2 h-16 w-full rounded-md bg-foreground/[.04] flex items-end gap-1 p-1">
                  {article.timeline.map((pt) => (
                    <div key={pt.date} className="flex-1 bg-foreground/40" style={{ height: `${pt.biasIndex}%` }} />
                  ))}
                </div>
              </div>
            )}
          </aside>
        </section>
      </div>
    </main>
  );
}


