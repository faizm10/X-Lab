'use client';

import jobsData from '../../data/jobs.json';
import { FilterPanel } from '@/components/FilterPanel';
import { JobCard } from '@/components/JobCard';
import { StatGrid } from '@/components/StatGrid';
import { useJobFilters } from '@/hooks/useJobFilters';
import type { Job } from '@/types/job';

const typedJobs = (jobsData as Job[]).sort(
  (a, b) => new Date(b.postedAt).getTime() - new Date(a.postedAt).getTime()
);

export default function Page() {
  const { filters, setFilters, filteredJobs, stats } = useJobFilters(typedJobs);

  const handleReset = () =>
    setFilters({
      search: '',
      companies: [],
      workModels: [],
      seniority: [],
      onlyActive: true,
    });

  return (
    <main className="shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Faiz Lab • talent radar</p>
          <h1>Intern &amp; early-career jobs, minus the noise</h1>
          <p>
            This lightweight frontend renders job data directly from{' '}
            <code>job-board/data/jobs.json</code>. Update the file, commit it, and the site
            redeploys—no backend hosting required.
          </p>
        </div>
        <div className="hero__cta">
          <a href="https://github.com/" target="_blank" rel="noreferrer" className="button">
            View Playbook
          </a>
          <a
            href="https://github.com/"
            target="_blank"
            rel="noreferrer"
            className="button button--ghost"
          >
            GitHub Actions plan
          </a>
        </div>
      </header>

      <StatGrid {...stats} />

      <FilterPanel jobs={typedJobs} filters={filters} onChange={setFilters} />

      <section className="panel job-panel">
        <div className="section-heading">
          <div>
            <p className="eyebrow subtle">Job feed</p>
            <h2>All curated roles</h2>
          </div>
          <span>{filteredJobs.length} listings</span>
        </div>

        <div className="job-grid">
          {filteredJobs.length === 0 ? (
            <div className="empty-state">
              <p>No job postings match your filters.</p>
              <button type="button" onClick={handleReset}>
                Reset filters
              </button>
            </div>
          ) : (
            filteredJobs.map((job) => <JobCard key={job.id} job={job} />)
          )}
        </div>
      </section>

      <section className="panel data-pipeline">
        <article>
          <h2>Data editing</h2>
          <ol>
            <li>Open <code>job-board/data/jobs.json</code>.</li>
            <li>Add, edit, or remove entries.</li>
            <li>Commit the change. The site updates instantly.</li>
          </ol>
        </article>
        <article>
          <h2>Scraper sync (optional)</h2>
          <p>
            Run <code>python backend/job-scraper/scrape_and_export.py</code> to scrape fresh
            roles and overwrite <code>jobs.json</code>. A GitHub Actions workflow can
            schedule this nightly and open an automated PR.
          </p>
        </article>
      </section>
    </main>
  );
}

