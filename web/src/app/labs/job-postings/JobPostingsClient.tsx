"use client";

import { useState } from "react";
import { JobPosting } from "../../../lib/api";
import JobFilter from "../../../components/JobFilter";

interface JobPostingsClientProps {
  companies: string[];
  initialJobs: JobPosting[];
  initialNewJobs: JobPosting[];
}

export default function JobPostingsClient({ 
  companies, 
  initialJobs
}: JobPostingsClientProps) {
  const [filteredJobs, setFilteredJobs] = useState<JobPosting[]>(initialJobs);
  const [loading, setLoading] = useState(false);

  return (
    <section className="mt-8">
      <h2 className="text-2xl font-semibold tracking-tight mb-4">Job Search</h2>
      
      <JobFilter 
        companies={companies}
        onJobsChange={setFilteredJobs}
        onLoadingChange={setLoading}
      />
      
      {/* Filtered Results */}
      <div className="mt-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold">
            {loading ? "Loading..." : `Found ${filteredJobs.length} jobs`}
          </h3>
        </div>
        
        {loading ? (
          <div className="text-center py-8">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <p className="mt-2 text-sm text-muted-foreground">Loading jobs...</p>
          </div>
        ) : filteredJobs.length > 0 ? (
          <div className="space-y-3">
            {filteredJobs.map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-muted-foreground">No jobs found matching your criteria.</p>
          </div>
        )}
      </div>
    </section>
  );
}

function JobCard({ job }: { job: JobPosting }) {
  return (
    <div className="bg-card border rounded-lg p-4 hover:shadow-md transition-shadow">
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
  );
}
