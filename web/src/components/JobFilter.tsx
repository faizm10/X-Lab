"use client";

import { useState, useEffect, useCallback } from "react";
import { fetchJobs, JobPosting, JobsResponse } from "../lib/api";

interface JobFilterProps {
  companies: string[];
  onJobsChange: (jobs: JobPosting[]) => void;
  onLoadingChange: (loading: boolean) => void;
}

export default function JobFilter({ companies, onJobsChange, onLoadingChange }: JobFilterProps) {
  const [selectedCompany, setSelectedCompany] = useState<string>("all");
  const [keywords, setKeywords] = useState<string>("");
  const [loading, setLoading] = useState(false);

  const fetchFilteredJobs = useCallback(async () => {
    setLoading(true);
    onLoadingChange(true);
    
    try {
      const params: {
        limit: number;
        active_only: boolean;
        company?: string;
        keywords?: string;
      } = {
        limit: 50,
        active_only: true
      };
      
      if (selectedCompany !== "all") {
        params.company = selectedCompany;
      }
      
      if (keywords.trim()) {
        params.keywords = keywords.trim();
      }
      
      const response: JobsResponse = await fetchJobs(params);
      onJobsChange(response.jobs);
    } catch (error) {
      console.error("Failed to fetch filtered jobs:", error);
      onJobsChange([]);
    } finally {
      setLoading(false);
      onLoadingChange(false);
    }
  }, [selectedCompany, keywords, onJobsChange, onLoadingChange]);

  useEffect(() => {
    fetchFilteredJobs();
  }, [fetchFilteredJobs]);

  return (
    <div className="bg-card border rounded-lg p-4 mb-6">
      <h3 className="text-lg font-semibold mb-4">Filter Jobs</h3>
      
      <div className="flex flex-col sm:flex-row gap-4">
        {/* Company Filter */}
        <div className="flex-1">
          <label htmlFor="company" className="block text-sm font-medium mb-2">
            Company
          </label>
          <select
            id="company"
            value={selectedCompany}
            onChange={(e) => setSelectedCompany(e.target.value)}
            className="w-full px-3 py-2 border rounded-md bg-background"
            disabled={loading}
          >
            <option value="all">All Companies</option>
            {companies.map((company) => (
              <option key={company} value={company}>
                {company}
              </option>
            ))}
          </select>
        </div>
        
        {/* Keywords Filter */}
        <div className="flex-1">
          <label htmlFor="keywords" className="block text-sm font-medium mb-2">
            Keywords (comma-separated)
          </label>
          <input
            id="keywords"
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="e.g., intern, internship, co-op"
            className="w-full px-3 py-2 border rounded-md bg-background"
            disabled={loading}
          />
        </div>
        
        {/* Refresh Button */}
        <div className="flex items-end">
          <button
            onClick={fetchFilteredJobs}
            disabled={loading}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50"
          >
            {loading ? "Loading..." : "Refresh"}
          </button>
        </div>
      </div>
    </div>
  );
}
