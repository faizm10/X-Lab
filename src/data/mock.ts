import type { ArticleDetail, ArticleSummary, NarrativeCluster, ApiList } from "@/types";

const now = new Date();

const scores = (s: Partial<ArticleSummary["scores"]>): ArticleSummary["scores"] => ({
  ideology: 50,
  factual: 75,
  framing: 50,
  emotion: 40,
  transparency: 65,
  ...s,
});

export const articles: ArticleDetail[] = [
  {
    id: "a1",
    title: "Federal Policy Shifts Spark Market Debate",
    outlet: "Global Ledger",
    author: "Ava Singh",
    publishedAt: new Date(now.getTime() - 3 * 60 * 60 * 1000).toISOString(),
    url: "https://example.com/a1",
    scores: scores({ ideology: 66, factual: 82, framing: 58, emotion: 36, transparency: 72 }),
    content:
      "Analysts disagreed on whether the policy would slow inflation. While some called it prudent, others warned of job losses. The administration framed the move as temporary stabilization.",
    highlights: [
      { start: 9, end: 18, dimension: "framing", score: 62, note: "disagreed" },
      { start: 94, end: 101, dimension: "ideology", score: 70, note: "warned" },
      { start: 132, end: 176, dimension: "framing", score: 64, note: "framed the move as" },
      { start: 177, end: 209, dimension: "emotion", score: 38, note: "temporary stabilization" },
    ],
    timeline: Array.from({ length: 14 }, (_, i) => ({
      date: new Date(now.getTime() - (13 - i) * 24 * 60 * 60 * 1000).toISOString(),
      biasIndex: 45 + Math.round(10 * Math.sin(i / 2)),
    })),
  },
  {
    id: "a2",
    title: "Regional Grid Faces Strain Amid Heatwave",
    outlet: "Northstar News",
    author: "Liam Zhou",
    publishedAt: new Date(now.getTime() - 26 * 60 * 60 * 1000).toISOString(),
    url: "https://example.com/a2",
    scores: scores({ ideology: 44, factual: 79, framing: 52, emotion: 48, transparency: 60 }),
    content:
      "Officials urged conservation as demand surged. Critics argued that deferred maintenance left systems vulnerable. Utilities said they were prepared for peak conditions.",
    highlights: [
      { start: 0, end: 8, dimension: "emotion", score: 52, note: "Officials urged" },
      { start: 54, end: 84, dimension: "factual", score: 80, note: "deferred maintenance" },
      { start: 118, end: 131, dimension: "framing", score: 55, note: "prepared" },
    ],
    timeline: Array.from({ length: 14 }, (_, i) => ({
      date: new Date(now.getTime() - (13 - i) * 24 * 60 * 60 * 1000).toISOString(),
      biasIndex: 52 + Math.round(8 * Math.cos(i / 2)),
    })),
  },
  {
    id: "a3",
    title: "New Study Maps Urban Transit Equity Gaps",
    outlet: "Civic Review",
    author: "Maya Ortiz",
    publishedAt: new Date(now.getTime() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    url: "https://example.com/a3",
    scores: scores({ ideology: 58, factual: 88, framing: 62, emotion: 34, transparency: 80 }),
    content:
      "Researchers identified disparities in access across neighborhoods. Advocates welcomed the findings, calling for targeted investment. City officials promised a comprehensive review.",
    highlights: [
      { start: 0, end: 11, dimension: "factual", score: 86, note: "Researchers identified" },
      { start: 85, end: 111, dimension: "emotion", score: 40, note: "welcomed the findings" },
      { start: 143, end: 167, dimension: "framing", score: 60, note: "comprehensive review" },
    ],
    timeline: Array.from({ length: 14 }, (_, i) => ({
      date: new Date(now.getTime() - (13 - i) * 24 * 60 * 60 * 1000).toISOString(),
      biasIndex: 48 + Math.round(12 * Math.sin(0.5 + i / 3)),
    })),
  },
];

export const articleSummaries: ApiList<ArticleSummary> = {
  items: articles.map((a) => ({
    id: a.id,
    title: a.title,
    outlet: a.outlet,
    publishedAt: a.publishedAt,
    url: a.url,
    scores: a.scores,
  })),
  updatedAt: now.toISOString(),
};

export const narratives: ApiList<NarrativeCluster> = {
  items: [
    {
      id: "n1",
      title: "Policy vs Markets",
      summary: "Debate over whether rate moves cool inflation without harming jobs.",
      keywords: ["inflation", "rates", "jobs", "stabilization"],
      intensity: 78,
      sentiment: 0.1,
      topArticles: articleSummaries.items.slice(0, 2),
      sparkline: [20, 28, 33, 45, 52, 49, 61, 66, 62, 58, 63, 72],
    },
    {
      id: "n2",
      title: "Grid Reliability",
      summary: "Heatwave pressures aging infrastructure; preparedness questioned.",
      keywords: ["grid", "heatwave", "maintenance", "peak"],
      intensity: 64,
      sentiment: -0.05,
      topArticles: [articleSummaries.items[1], articleSummaries.items[2]],
      sparkline: [12, 14, 18, 19, 23, 27, 31, 29, 34, 36, 42, 48],
    },
    {
      id: "n3",
      title: "Transit Equity",
      summary: "Study highlights uneven access; calls for targeted investment.",
      keywords: ["transit", "equity", "access", "investment"],
      intensity: 55,
      sentiment: 0.2,
      topArticles: [articleSummaries.items[2], articleSummaries.items[0]],
      sparkline: [10, 11, 13, 17, 18, 20, 23, 22, 25, 27, 29, 35],
    },
  ],
  updatedAt: now.toISOString(),
};


