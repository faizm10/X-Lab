export type BiasDimension =
  | "ideology"
  | "factual"
  | "framing"
  | "emotion"
  | "transparency";

export type BiasScores = Record<BiasDimension, number>; // 0..100

export interface HighlightSpan {
  start: number;
  end: number;
  dimension: BiasDimension;
  score: number;
  note?: string;
}

export interface ArticleSummary {
  id: string;
  title: string;
  outlet: string;
  publishedAt: string; // ISO
  url: string; // primary source
  scores: BiasScores;
}

export interface ArticleDetail extends ArticleSummary {
  author?: string;
  content: string; // plain text for prototype
  highlights: HighlightSpan[];
  timeline?: Array<{ date: string; biasIndex: number }>; // for bonus chart
}

export interface NarrativeCluster {
  id: string;
  title: string;
  summary: string;
  keywords: string[];
  intensity: number; // 0..100 influences bubble size
  sentiment: number; // -1..1
  topArticles: ArticleSummary[];
  sparkline: number[]; // last N periods [0..100]
}

export interface ApiList<T> {
  items: T[];
  updatedAt: string;
}


