"use client";

import Link from "next/link";
import { useState, useEffect } from "react";
import { tools } from "../../../data/mock";
import { fetchJobs, fetchStats, fetchNewJobsToday, type JobPosting, type StatsResponse } from "../../../lib/api";

export default function AutomaticJobAlerts() {
  const [selectedFilter, setSelectedFilter] = useState<"all" | "new">("all");
  const [selectedCompany, setSelectedCompany] = useState<"all" | "Microsoft">("all");
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const tool = tools.items.find((n) => n.id === "automatic-job-alerts");
  
  // Helper function to get the most relevant date for sorting
  // Prioritize posted_date (actual company posting date) over first_seen (when we discovered it)
  const getRelevantDate = (job: JobPosting): Date => {
    if (job.posted_date) {
      return new Date(job.posted_date);
    }
    return new Date(job.first_seen);
  };

  // Sort jobs by most recent posting date
  const sortJobsByDate = (jobs: JobPosting[]): JobPosting[] => {
    return [...jobs].sort((a, b) => 
      getRelevantDate(b).getTime() - getRelevantDate(a).getTime()
    );
  };
  
  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedFilter, selectedCompany]);

  async function loadData() {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch stats
      const statsData = await fetchStats();
      setStats(statsData);
      
      // Fetch jobs based on time filter and company filter
      if (selectedFilter === "new") {
        if (selectedCompany === "all") {
          // Fetch all new jobs from today without company filter
          const newJobs = await fetchNewJobsToday();
          setJobs(sortJobsByDate(newJobs.jobs));
        } else {
          const newJobs = await fetchNewJobsToday(selectedCompany);
          setJobs(sortJobsByDate(newJobs.jobs));
        }
      } else {
        if (selectedCompany === "all") {
          // Fetch all jobs without company filter - this will get ALL jobs from the API
          const jobsData = await fetchJobs({
            active_only: true,
            limit: 500, // Increased limit to get all jobs
          });
          // Sort by posting date (when available) or first_seen date (newest first)
          setJobs(sortJobsByDate(jobsData.jobs));
        } else {
          const jobsData = await fetchJobs({
            company: selectedCompany,
            active_only: true,
            limit: 100,
          });
          setJobs(sortJobsByDate(jobsData.jobs));
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load data");
      console.error("Error loading data:", err);
    } finally {
      setLoading(false);
    }
  }
  
  if (!tool) {
    return (
      <main className="min-h-dvh bg-background text-foreground">
        <div className="mx-auto max-w-5xl px-6 md:px-10 py-12">Tool not found</div>
      </main>
    );
  }

  const isNew = (job: JobPosting) => {
    const firstSeen = new Date(job.first_seen);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return firstSeen >= today;
  };

  const lastScrapedAt = stats?.last_scraped ? new Date(stats.last_scraped) : new Date();

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
            <div className="mt-2 text-3xl font-semibold">
              {loading ? "..." : stats?.total_jobs ?? 0}
            </div>
          </div>
          
          <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
            <div className="text-sm text-foreground/60">New Today</div>
            <div className="mt-2 text-3xl font-semibold text-green-500">
              {loading ? "..." : stats?.new_today ?? 0}
            </div>
          </div>

          <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
            <div className="text-sm text-foreground/60">Companies Tracked</div>
            <div className="mt-2 text-3xl font-semibold">
              {loading ? "..." : stats?.companies_tracked ?? 0}
            </div>
            <div className="mt-1 text-xs text-foreground/50">
              {stats?.companies.join(", ") ?? "Microsoft"}
            </div>
          </div>

          <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6">
            <div className="text-sm text-foreground/60">Last Scraped</div>
            <div className="mt-2 text-sm font-medium">
              {loading ? "..." : lastScrapedAt.toLocaleTimeString()}
            </div>
            <div className="mt-1 text-xs text-foreground/50">
              {loading ? "" : lastScrapedAt.toLocaleDateString()}
            </div>
          </div>
        </section>

        {/* Controls */}
        <section className="mt-12">
          <div className="flex flex-col gap-4">
            <div className="flex items-center justify-between flex-wrap gap-4">
              <h2 className="text-2xl font-semibold tracking-tight">
                Job Postings
              </h2>
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => setSelectedFilter("all")}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedFilter === "all"
                      ? "bg-foreground text-background"
                      : "bg-foreground/5 hover:bg-foreground/10"
                  }`}
                >
                  All ({loading ? "..." : stats?.total_jobs ?? 0})
                </button>
                <button
                  onClick={() => setSelectedFilter("new")}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedFilter === "new"
                      ? "bg-foreground text-background"
                      : "bg-foreground/5 hover:bg-foreground/10"
                  }`}
                >
                  New ({loading ? "..." : stats?.new_today ?? 0})
                </button>
              </div>
            </div>
            
            {/* Company Filter */}
            <div className="flex items-center gap-2">
              <span className="text-sm text-foreground/60">Company:</span>
              <div className="flex gap-2">
                <button
                  onClick={() => setSelectedCompany("all")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    selectedCompany === "all"
                      ? "bg-foreground text-background"
                      : "bg-foreground/5 hover:bg-foreground/10"
                  }`}
                >
                  All Companies
                </button>
                <button
                  onClick={() => setSelectedCompany("Microsoft")}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                    selectedCompany === "Microsoft"
                      ? "bg-indigo-500 text-white"
                      : "bg-indigo-500/10 text-indigo-600 hover:bg-indigo-500/20 dark:text-indigo-400"
                  }`}
                >
                  Microsoft
                </button>
              </div>
            </div>
            
            {/* Info Banner */}
            <div className="flex flex-col gap-3 p-4 rounded-lg bg-indigo-500/5 border border-indigo-500/20">
              <div className="flex items-center justify-between flex-wrap gap-2">
                <div className="flex items-center gap-2 text-sm font-medium text-indigo-600 dark:text-indigo-400">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>Scraper Configuration</span>
                </div>
                <div className="flex items-center gap-1.5 flex-wrap">
                  <span className="px-2.5 py-1 text-xs font-semibold bg-indigo-500/20 text-indigo-600 dark:text-indigo-400 rounded-full">Microsoft</span>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex items-start gap-2 text-sm text-foreground/70">
                  <svg className="w-4 h-4 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                  <div>
                    <strong>Microsoft:</strong> Software Engineering internships for students and graduates
                    <div className="mt-0.5 text-xs text-foreground/60">
                      Includes: Azure Data, Applied AI/ML, Frontend, Fullstack, Systems, Security, and more
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Job Listings */}
        <section className="mt-6 space-y-3">
          {!loading && !error && jobs.length > 0 && (
            <div className="text-sm text-foreground/60 pb-2">
              Showing <span className="font-semibold text-foreground">{jobs.length}</span> {jobs.length === 1 ? 'job' : 'jobs'}
              {selectedCompany !== "all" && <span> from <span className="font-semibold text-foreground">{selectedCompany}</span></span>}
            </div>
          )}
          {error && (
            <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-6 text-center">
              <p className="text-red-500">{error}</p>
              <button
                onClick={loadData}
                className="mt-4 px-4 py-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-500 text-sm font-medium transition-colors"
              >
                Retry
              </button>
            </div>
          )}
          
          {loading ? (
            <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-12 text-center">
              <p className="text-foreground/60">Loading jobs...</p>
            </div>
          ) : jobs.length === 0 ? (
            <div className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-12 text-center">
              <p className="text-foreground/60">No job postings found</p>
            </div>
          ) : (
            jobs.map((job) => (
              <div
                key={job.id}
                className="rounded-xl border border-foreground/10 bg-foreground/[0.02] p-6 hover:bg-foreground/[0.04] transition-colors group"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start gap-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="px-2.5 py-1 text-xs font-semibold bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 rounded-md">
                            {job.company}
                          </span>
                          {isNew(job) && (
                            <span className="px-2 py-0.5 text-xs font-medium bg-green-500/10 text-green-500 rounded-full">
                              NEW
                            </span>
                          )}
                        </div>
                        <h3 className="text-lg font-semibold group-hover:text-foreground/80 transition-colors mb-2">
                          {job.title}
                        </h3>
                        <div className="flex items-center gap-4 text-sm text-foreground/60">
                          {job.team && (
                            <span className="flex items-center gap-1">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                              </svg>
                              <span>{job.team}</span>
                            </span>
                          )}
                          {job.location && (
                            <span className="flex items-center gap-1">
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                              </svg>
                              {job.location}
                            </span>
                          )}
                          <span className="flex items-center gap-1" title={job.posted_date ? "Date posted by company" : "Date first discovered by scraper"}>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            {job.posted_date 
                              ? `Posted ${new Date(job.posted_date).toLocaleDateString()}`
                              : `First seen ${new Date(job.first_seen).toLocaleDateString()}`
                            }
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
            <p>• 🎯 <strong>Smart Filtering:</strong> Filter by company, view all jobs or only new ones</p>
            <p>• 📊 <strong>Analytics:</strong> Track posting patterns and application timelines</p>
          </div>
          
          <div className="mt-6 pt-6 border-t border-foreground/10">
            <h4 className="text-sm font-semibold mb-2">Currently Tracking:</h4>
            <div className="flex flex-wrap gap-2">
              <span className="px-3 py-1.5 rounded-lg bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 text-xs font-medium">
                Microsoft Internships (Students & Graduates)
              </span>
              <span className="px-3 py-1.5 rounded-lg bg-foreground/5 text-foreground/40 text-xs">
                + More companies coming soon
              </span>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}

