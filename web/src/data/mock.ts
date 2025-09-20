import type { Lab, ApiList } from "../types";

const now = new Date();

// Placeholder data for labs - clean and minimal
export const placeholderProjects = [
  {
    id: "project-1",
    title: "Transit Cost Analysis",
    outlet: "Data Lab",
    publishedAt: new Date(now.getTime() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    url: "#",
    scores: { ideology: 50, factual: 85, framing: 60, emotion: 45, transparency: 80 },
  },
  {
    id: "project-2", 
    title: "Route Optimization Study",
    outlet: "Data Lab",
    publishedAt: new Date(now.getTime() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    url: "#",
    scores: { ideology: 45, factual: 90, framing: 55, emotion: 40, transparency: 85 },
  },
];

export const labs: ApiList<Lab> = {
  items: [
    {
      id: "go-transit-costs",
      title: "GO Transit - Costs",
      summary: "Analyze cost/time tradeoffs for train+bus vs bus+bus commuting patterns.",
      keywords: ["transit", "cost", "time", "commute", "optimization"],
      intensity: 85,
      sentiment: 0.3,
      topArticles: placeholderProjects,
      sparkline: [45, 52, 48, 61, 58, 63, 72, 68, 75, 71, 78, 82],
    },
    {
      id: "referee-decision-bias",
      title: "Referee Decision Bias",
      summary: "Collect match officiating events (fouls, yellows, reds, penalties) and quantify whether decisions skew for home vs away, popular vs less-popular teams, or specific players. Expose an API, run batch audits, and produce bias metrics with significance tests.",
      keywords: ["football", "soccer", "referee", "bias", "fairness", "home advantage", "statistics", "chi-square", "logistic-regression"],
      intensity: 85,
      sentiment: 0.3,
      topArticles: placeholderProjects,
      sparkline: [45, 52, 48, 61, 58, 63, 72, 68, 75, 71, 78, 82],
    },
  ],
  updatedAt: now.toISOString(),
};


