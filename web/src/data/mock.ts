import type { Lab, Tool, ApiList } from "../types";

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
      id: "job-postings",
      title: "Job Postings",
      summary: "Under Construction",
      keywords: ["jobs", "automation", "alerts"],
      intensity: 75,
      sentiment: 0.4,
      topArticles: placeholderProjects,
      sparkline: [40, 45, 48, 52, 55, 58, 62, 65, 68, 70, 72, 75],
    },
  ],
  updatedAt: now.toISOString(),
};

export const tools: ApiList<Tool> = {
  items: [
    {
      id: "automatic-job-alerts",
      title: "Automatic Job Alerts",
      summary: "Real-time monitoring of job postings from top companies. Get notified instantly when new positions are posted so you can apply right away.",
      keywords: ["automation", "web scraping", "job alerts", "real-time"],
      intensity: 90,
      sentiment: 0.5,
      topArticles: placeholderProjects,
      sparkline: [32, 38, 41, 45, 52, 58, 64, 71, 75, 82, 88, 90],
    },
  ],
  updatedAt: now.toISOString(),
};

// Export articles for backwards compatibility
export const articles = placeholderProjects.map(p => ({
  ...p,
  content: "Sample article content",
  highlights: [],
  author: "Data Lab",
  timeline: [
    { date: "2024-01", biasIndex: 45 },
    { date: "2024-02", biasIndex: 52 },
    { date: "2024-03", biasIndex: 48 },
    { date: "2024-04", biasIndex: 61 },
  ],
}));

