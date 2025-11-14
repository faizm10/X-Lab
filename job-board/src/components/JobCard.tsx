import { BadgeCheck, Briefcase, Link as LinkIcon, MapPin, Share2 } from "lucide-react";
import type { Job } from "../types/job";

interface JobCardProps {
  job: Job;
}

const workModelCopy: Record<Job["workModel"], string> = {
  remote: "Remote",
  hybrid: "Hybrid",
  onsite: "On-site",
};

export function JobCard({ job }: JobCardProps) {
  const postedDate = new Date(job.postedAt).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });

  return (
    <article className="job-card">
      <header className="job-card__header">
        <div>
          <p className="job-card__company">
            {job.company}
            {job.isActive ? (
              <BadgeCheck size={16} aria-label="Active posting" />
            ) : (
              <span className="job-card__inactive">Archived</span>
            )}
          </p>
          <h3>{job.title}</h3>
        </div>
        <a
          className="job-card__apply"
          href={job.applyUrl}
          target="_blank"
          rel="noreferrer"
        >
          Apply <Share2 size={16} />
        </a>
      </header>

      <div className="job-card__meta">
        <span>
          <MapPin size={16} /> {job.location}
        </span>
        <span>
          <Briefcase size={16} /> {workModelCopy[job.workModel]}
        </span>
        <span>
          <LinkIcon size={16} /> Posted {postedDate}
        </span>
      </div>

      {job.description && <p className="job-card__description">{job.description}</p>}

      <footer className="job-card__footer">
        <div className="job-card__tags">
          {(job.tags ?? []).map((tag) => (
            <span key={tag}>{tag}</span>
          ))}
        </div>
        {job.salaryRange && (
          <p className="job-card__salary">
            {job.salaryRange.currency ?? "CAD"} {job.salaryRange.min ?? "—"}
            {job.salaryRange.max ? ` - ${job.salaryRange.max}` : ""} /
            {job.salaryRange.cadence ?? "annual"}
          </p>
        )}
      </footer>
    </article>
  );
}

