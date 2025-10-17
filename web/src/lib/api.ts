const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

export interface JobPosting {
  id: string;
  company: string;
  title: string;
  team: string | null;
  location: string | null;
  url: string;
  description: string | null;
  first_seen: string;
  last_seen: string;
  is_active: boolean;
  posted_date: string | null;
  scraped_count: number;
}

export interface JobsResponse {
  total: number;
  limit: number;
  offset: number;
  jobs: JobPosting[];
}

export interface StatsResponse {
  total_jobs: number;
  active_jobs: number;
  new_today: number;
  new_this_week: number;
  companies_tracked: number;
  companies: string[];
  last_scraped: string | null;
}

export interface NewJobsResponse {
  date: string;
  count: number;
  jobs: JobPosting[];
}

export async function fetchJobs(params?: {
  company?: string;
  active_only?: boolean;
  limit?: number;
  offset?: number;
}): Promise<JobsResponse> {
  const searchParams = new URLSearchParams();
  
  if (params?.company) searchParams.set("company", params.company);
  if (params?.active_only !== undefined) searchParams.set("active_only", String(params.active_only));
  if (params?.limit) searchParams.set("limit", String(params.limit));
  if (params?.offset) searchParams.set("offset", String(params.offset));
  
  const url = `${API_BASE_URL}/api/jobs${searchParams.toString() ? `?${searchParams.toString()}` : ""}`;
  
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch jobs: ${response.statusText}`);
  }
  
  return response.json();
}

export async function fetchStats(): Promise<StatsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/stats`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch stats: ${response.statusText}`);
  }
  
  return response.json();
}

export async function fetchNewJobsToday(company?: string): Promise<NewJobsResponse> {
  const url = company 
    ? `${API_BASE_URL}/api/jobs/new/today?company=${company}`
    : `${API_BASE_URL}/api/jobs/new/today`;
  
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });
  
  if (!response.ok) {
    throw new Error(`Failed to fetch new jobs: ${response.statusText}`);
  }
  
  return response.json();
}

export async function triggerScrape(company: string = "stripe"): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/scrape?company=${company}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });
  
  if (!response.ok) {
    throw new Error(`Failed to trigger scrape: ${response.statusText}`);
  }
}

