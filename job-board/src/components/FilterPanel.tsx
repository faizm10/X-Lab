import type { FilterState } from "../hooks/useJobFilters";
import type { Job, WorkModel, JobSeniority } from "../types/job";

interface FilterPanelProps {
  jobs: Job[];
  filters: FilterState;
  onChange: (filters: FilterState) => void;
}

const workModelOptions: { label: string; value: WorkModel }[] = [
  { label: "Remote", value: "remote" },
  { label: "Hybrid", value: "hybrid" },
  { label: "On-site", value: "onsite" },
];

const seniorityOptions: { label: string; value: JobSeniority }[] = [
  { label: "Internships", value: "internship" },
  { label: "Co-ops", value: "co-op" },
  { label: "New Grad", value: "new-grad" },
  { label: "Contracts", value: "contract" },
];

export function FilterPanel({ jobs, filters, onChange }: FilterPanelProps) {
  const companies = Array.from(new Set(jobs.map((job) => job.company))).sort();

  const toggleValue = <T extends string>(collection: T[], value: T): T[] => {
    return collection.includes(value)
      ? collection.filter((item) => item !== value)
      : [...collection, value];
  };

  return (
    <section className="filters">
      <div className="filters__row">
        <div className="filters__group">
          <label htmlFor="search">Search</label>
          <input
            id="search"
            type="search"
            placeholder="Search by role, stack, or city"
            value={filters.search}
            onChange={(event) =>
              onChange({
                ...filters,
                search: event.target.value,
              })
            }
          />
        </div>
        <div className="filters__group">
          <label htmlFor="company">Company</label>
          <select
            id="company"
            value={filters.companies[0] ?? ""}
            onChange={(event) =>
              onChange({
                ...filters,
                companies: event.target.value ? [event.target.value] : [],
              })
            }
          >
            <option value="">Any</option>
            {companies.map((company) => (
              <option key={company} value={company}>
                {company}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="filters__row">
        <fieldset className="filters__group">
          <legend>Workstyle</legend>
          <div className="chip-row">
            {workModelOptions.map((option) => (
              <button
                key={option.value}
                className={`chip ${filters.workModels.includes(option.value) ? "chip--active" : ""}`}
                onClick={() =>
                  onChange({
                    ...filters,
                    workModels: toggleValue(filters.workModels, option.value),
                  })
                }
                type="button"
              >
                {option.label}
              </button>
            ))}
          </div>
        </fieldset>

        <fieldset className="filters__group">
          <legend>Seniority</legend>
          <div className="chip-row">
            {seniorityOptions.map((option) => (
              <button
                key={option.value}
                className={`chip ${filters.seniority.includes(option.value) ? "chip--active" : ""}`}
                onClick={() =>
                  onChange({
                    ...filters,
                    seniority: toggleValue(filters.seniority, option.value),
                  })
                }
                type="button"
              >
                {option.label}
              </button>
            ))}
          </div>
        </fieldset>
      </div>

      <label className="toggle">
        <input
          type="checkbox"
          checked={filters.onlyActive}
          onChange={(event) =>
            onChange({
              ...filters,
              onlyActive: event.target.checked,
            })
          }
        />
        Show active postings only
      </label>
    </section>
  );
}

