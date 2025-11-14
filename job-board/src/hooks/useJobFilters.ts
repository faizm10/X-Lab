import { useMemo, useState } from "react";
import type { Job, WorkModel, JobSeniority } from "../types/job";

export interface FilterState {
  search: string;
  companies: string[];
  workModels: WorkModel[];
  seniority: JobSeniority[];
  onlyActive: boolean;
}

const defaultState: FilterState = {
  search: "",
  companies: [],
  workModels: [],
  seniority: [],
  onlyActive: true,
};

export function useJobFilters(jobs: Job[]) {
  const [filters, setFilters] = useState<FilterState>(defaultState);

  const filteredJobs = useMemo(() => {
    return jobs.filter((job) => {
      if (filters.onlyActive && !job.isActive) {
        return false;
      }

      if (filters.companies.length && !filters.companies.includes(job.company)) {
        return false;
      }

      if (filters.workModels.length && !filters.workModels.includes(job.workModel)) {
        return false;
      }

      if (filters.seniority.length && !filters.seniority.includes(job.seniority)) {
        return false;
      }

      if (filters.search.trim()) {
        const query = filters.search.toLowerCase();
        const haystack = [
          job.company,
          job.title,
          job.location,
          job.team,
          job.discipline,
          ...(job.tags ?? []),
        ]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();

        if (!haystack.includes(query)) {
          return false;
        }
      }

      return true;
    });
  }, [jobs, filters]);

  const stats = useMemo(() => {
    const active = filteredJobs.filter((job) => job.isActive).length;
    const remote = filteredJobs.filter((job) => job.workModel === "remote").length;
    const cities = new Set(filteredJobs.map((job) => job.location));

    return {
      total: filteredJobs.length,
      active,
      remote,
      cities: cities.size,
    };
  }, [filteredJobs]);

  return {
    filters,
    setFilters,
    filteredJobs,
    stats,
  };
}

