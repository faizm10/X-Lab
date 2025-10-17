"use client";

import Link from "next/link";
import { useState } from "react";
import { tools } from "../../../data/mock";

interface JobPosting {
  id: string;
  title: string;
  team: string;
  location: string;
  url: string;
  postedAt: string;
  isNew: boolean;
}

// Mock job postings - will be replaced with real scraping data
const mockJobPostings: JobPosting[] = [
  {
    id: "7285986",
    title: "Data Analyst, Intern (Master's degree)",
    team: "University",
    location: "Toronto",
    url: "https://stripe.com/jobs/listing/data-analyst-intern-master-s-degree/7285986",
    postedAt: "2025-10-16T14:30:00Z",
    isNew: true,
  },
  {
    id: "7285974",
    title: "PhD Data Scientist, Intern",
    team: "University",
    location: "Toronto",
    url: "https://stripe.com/jobs/listing/phd-data-scientist-intern/7285974",
    postedAt: "2025-10-16T14:30:00Z",
    isNew: true,
  },
  {
    id: "7216664",
    title: "PhD Machine Learning Engineer, Intern",
    team: "University",
    location: "South San Francisco HQ",
    url: "https://stripe.com/jobs/listing/phd-machine-learning-engineer-intern/7216664",
    postedAt: "2025-10-15T10:20:00Z",
    isNew: false,
  },
  {
    id: "7206401",
    title: "Software Engineer, Intern",
    team: "University",
    location: "Singapore",
    url: "https://stripe.com/jobs/listing/software-engineer-intern/7206401",
    postedAt: "2025-10-14T09:15:00Z",
    isNew: false,
  },
  {
    id: "7210115",
    title: "Software Engineer, Intern (Summer and Winter)",
    team: "University",
    location: "Seattle",
    url: "https://stripe.com/jobs/listing/software-engineer-intern-summer-and-winter/7210115",
    postedAt: "2025-10-13T16:45:00Z",
    isNew: false,
  },
];

export default function AutomaticJobAlerts() {
  const [selectedFilter, setSelectedFilter] = useState<"all" | "new">("all");
  const tool = tools.items.find((n) => n.id === "automatic-job-alerts");
  
  if (!tool) {
    return (
      <main className="min-h-dvh bg-background text-foreground">
        <div className="mx-auto max-w-5xl px-6 md:px-10 py-12">Tool not found</div>
      </main>
    );
  }

  const filteredPostings = selectedFilter === "new" 
    ? mockJobPostings.filter(job => job.isNew)
    : mockJobPostings;

  const newJobsCount = mockJobPostings.filter(job => job.isNew).length;
  const lastScrapedAt = new Date();

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 py-12 md:py-16">
        <div className="flex items-center justify-between">
          <Link href="/tools" className="text-sm hover:opacity-70 transition-opacity">
            ← Tools
          </Link>
        </div>
        
        <header className="mt-6">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-5xl font-semibold tracking-tight">
                {tool.title}
              </h1>
              <p className="mt-3 text-foreground/70 max-w-2xl text-base">
                {tool.summary}
              </p>
            </div>
            <div className="flex items-center gap-2 text-xs text-foreground/60">
              <div className="h-2 w-2 rounded-full bg-green-500 animate-pulse" />
              <span>Live Monitoring</span>
            </div>
          </div>
          
          <div className="mt-4 flex flex-wrap gap-2">
            {tool.keywords.map((k) => (
              <span 
                key={k} 
                className="rounded-full border border-foreground/10 px-3 py-1 text-xs text-foreground/70"
              >
                {k}
              </span>
            ))}
          </div>
        </header>

        {/* Stats Section */}
        <section className="mt-12 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
            <div className="text-sm text-foreground/60">Total Postings</div>
            <div className="mt-2 text-3xl font-semibold">{mockJobPostings.length}</div>
          </div>
          
          <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
            <div className="text-sm text-foreground/60">New Today</div>
            <div className="mt-2 text-3xl font-semibold text-green-500">
              {newJobsCount}
            </div>
          </div>

          <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
            <div className="text-sm text-foreground/60">Companies Tracked</div>
            <div className="mt-2 text-3xl font-semibold">1</div>
            <div className="mt-1 text-xs text-foreground/50">Stripe</div>
          </div>

          <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
            <div className="text-sm text-foreground/60">Last Scraped</div>
            <div className="mt-2 text-sm font-medium">
              {lastScrapedAt.toLocaleTimeString()}
            </div>
            <div className="mt-1 text-xs text-foreground/50">
              {lastScrapedAt.toLocaleDateString()}
            </div>
          </div>
        </section>

        {/* Controls */}
        <section className="mt-12">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-semibold tracking-tight">
              Job Postings
            </h2>
            <div className="flex gap-2">
              <button
                onClick={() => setSelectedFilter("all")}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFilter === "all"
                    ? "bg-foreground text-background"
                    : "bg-foreground/5 hover:bg-foreground/10"
                }`}
              >
                All ({mockJobPostings.length})
              </button>
              <button
                onClick={() => setSelectedFilter("new")}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  selectedFilter === "new"
                    ? "bg-foreground text-background"
                    : "bg-foreground/5 hover:bg-foreground/10"
                }`}
              >
                New ({newJobsCount})
              </button>
            </div>
          </div>
        </section>

        {/* Job Listings */}
        <section className="mt-6 space-y-3">
          {filteredPostings.length === 0 ? (
            <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-12 text-center">
              <p className="text-foreground/60">No job postings found</p>
            </div>
          ) : (
            filteredPostings.map((job) => (
              <div
                key={job.id}
                className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6 hover:bg-foreground/[0.04] transition-colors group"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start gap-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <h3 className="text-lg font-semibold group-hover:text-foreground/80 transition-colors">
                            {job.title}
                          </h3>
                          {job.isNew && (
                            <span className="px-2 py-0.5 text-xs font-medium bg-green-500/10 text-green-500 rounded-full">
                              NEW
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-4 text-sm text-foreground/60">
                          <span className="flex items-center gap-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            {job.team}
                          </span>
                          <span className="flex items-center gap-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            {job.location}
                          </span>
                          <span className="flex items-center gap-1">
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {new Date(job.postedAt).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <a
                    href={job.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-4 py-2 rounded-lg bg-foreground text-background text-sm font-medium hover:opacity-80 transition-opacity whitespace-nowrap"
                  >
                    Apply →
                  </a>
                </div>
              </div>
            ))
          )}
        </section>

        {/* Info Section */}
        <section className="mt-12 rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
          <h3 className="text-lg font-semibold mb-3">How it works</h3>
          <div className="space-y-2 text-sm text-foreground/70">
            <p>• 🔍 <strong>Automatic Scraping:</strong> Checks for new postings every hour</p>
            <p>• 🔔 <strong>Instant Notifications:</strong> Get alerted immediately when new jobs are posted</p>
            <p>• 🎯 <strong>Smart Filtering:</strong> Currently tracking Stripe internships</p>
            <p>• 📊 <strong>Analytics:</strong> Track posting patterns and application timelines</p>
          </div>
          
          <div className="mt-6 pt-6 border-t border-foreground/10">
            <h4 className="text-sm font-semibold mb-2">Currently Tracking:</h4>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1.5 rounded-lg bg-indigo-500/10 text-indigo-500 text-xs font-medium">
                Stripe Internships
              </span>
              <span className="px-3 py-1.5 rounded-lg bg-foreground/5 text-foreground/40 text-xs">
                + More coming soon
              </span>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

