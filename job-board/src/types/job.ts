export type JobSeniority = "internship" | "new-grad" | "co-op" | "contract";
export type WorkModel = "remote" | "hybrid" | "onsite";

export interface Job {
  id: string;
  company: string;
  title: string;
  location: string;
  workModel: WorkModel;
  team?: string;
  discipline?: string;
  description?: string;
  tags?: string[];
  postedAt: string;
  applyUrl: string;
  salaryRange?: {
    min?: number;
    max?: number;
    currency?: string;
    cadence?: "hourly" | "annual" | "monthly";
  };
  seniority: JobSeniority;
  isActive: boolean;
}

