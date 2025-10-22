import Link from "next/link";
import { labs } from "../../../data/mock";
import { fetchJobs, fetchStats, fetchNewJobsToday, JobPosting, StatsResponse } from "../../../lib/api";
import JobPostingsClient from "./JobPostingsClient";

export const dynamic = "force-dynamic";

export default async function JobPostingsPage() {
  const { items } = labs;
  const lab = items.find((n) => n.id === "job-postings");
  
  if (!lab) {
    return (
      <main className="min-h-dvh bg-background text-foreground">
        <div className="mx-auto max-w-5xl px-6 md:px-10 py-12">Lab not found</div>
      </main>
    );
  }

  // Fetch data from the API
  let stats: StatsResponse;
  let recentJobs: JobPosting[] = [];
  let newJobsToday: JobPosting[] = [];

  try {
    stats = await fetchStats();
    const jobsResponse = await fetchJobs({ limit: 20 });
    recentJobs = jobsResponse.jobs;
    const newJobsResponse = await fetchNewJobsToday();
    newJobsToday = newJobsResponse.jobs;
  } catch (error) {
    console.error("Failed to fetch job data:", error);
    // Fallback data
    stats = {
      total_jobs: 0,
      active_jobs: 0,
      new_today: 0,
      new_this_week: 0,
      companies_tracked: 0,
      companies: [],
      last_scraped: null
    };
  }

  return (
    <main className="min-h-dvh bg-background text-foreground">
      <div className="mx-auto max-w-7xl px-6 md:px-10 py-12 md:py-16">
        <div className="flex items-center justify-between">
          <Link href="/labs" className="text-sm hover:opacity-70">← Labs</Link>
        </div>
        
        <header className="mt-6">
          <h1 className="text-3xl md:text-5xl font-semibold tracking-tight">{lab.title}</h1>
          <p className="mt-3 text-foreground/70 max-w-2xl text-base">{lab.summary}</p>
          
          <div className="mt-4 flex flex-wrap gap-2">
            {lab.keywords.map((k) => (
              <span key={k} className="rounded-full border border-foreground/10 px-3 py-1 text-xs text-foreground/70">{k}</span>
            ))}
          </div>
        </header>

        {/* Stats Overview */}
        <section className="mt-12">
          <h2 className="text-2xl font-semibold tracking-tight mb-6">Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-card border rounded-lg p-4">
              <div className="text-2xl font-bold">{stats.total_jobs}</div>
              <div className="text-sm text-muted-foreground">Total Jobs</div>
            </div>
            <div className="bg-card border rounded-lg p-4">
              <div className="text-2xl font-bold">{stats.active_jobs}</div>
              <div className="text-sm text-muted-foreground">Active Jobs</div>
            </div>
            <div className="bg-card border rounded-lg p-4">
              <div className="text-2xl font-bold">{stats.new_today}</div>
              <div className="text-sm text-muted-foreground">New Today</div>
            </div>
            <div className="bg-card border rounded-lg p-4">
              <div className="text-2xl font-bold">{stats.companies_tracked}</div>
              <div className="text-sm text-muted-foreground">Companies</div>
            </div>
          </div>
        </section>

        {/* Companies Tracked */}
        <section className="mt-8">
          <h2 className="text-2xl font-semibold tracking-tight mb-4">Companies Tracked</h2>
          <div className="flex flex-wrap gap-2">
            {stats.companies.map((company) => (
              <span key={company} className="rounded-full bg-primary/10 px-3 py-1 text-sm font-medium">
                {company}
              </span>
            ))}
          </div>
        </section>

        {/* New Jobs Today */}
        {newJobsToday.length > 0 && (
          <section className="mt-8">
            <h2 className="text-2xl font-semibold tracking-tight mb-4">New Jobs Today ({newJobsToday.length})</h2>
            <div className="space-y-3">
              {newJobsToday.slice(0, 5).map((job) => (
                <div key={job.id} className="bg-card border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="font-semibold text-lg">{job.title}</span>
                        <span className="bg-primary/10 text-primary px-2 py-1 rounded text-sm font-medium">
                          {job.company}
                        </span>
                      </div>
                      {job.team && (
                        <p className="text-sm text-muted-foreground mb-1">Team: {job.team}</p>
                      )}
                      {job.location && (
                        <p className="text-sm text-muted-foreground mb-2">📍 {job.location}</p>
                      )}
                      <div className="flex items-center gap-4 text-xs text-muted-foreground">
                        <span>First seen: {new Date(job.first_seen).toLocaleDateString()}</span>
                        <span>Scraped {job.scraped_count} times</span>
                      </div>
                    </div>
                    <div className="ml-4">
                      <a
                        href={job.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-primary text-primary-foreground px-3 py-1 rounded text-sm hover:bg-primary/90 transition-colors"
                      >
                        View Job
                      </a>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        {/* Job Filter and Results */}
        <JobPostingsClient 
          companies={stats.companies}
          initialJobs={recentJobs}
          initialNewJobs={newJobsToday}
        />

        {/* Last Updated */}
        {stats.last_scraped && (
          <section className="mt-8">
            <p className="text-sm text-muted-foreground">
              Last updated: {new Date(stats.last_scraped).toLocaleString()}
            </p>
          </section>
        )}
      </div>
    </main>
  );
}
