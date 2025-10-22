# Labs Directory Structure

This directory contains individual lab pages with custom layouts. Each lab has its own unique identifier and can have a completely different layout and functionality.

## Current Labs

### `job-postings/`
- **Route**: `/labs/job-postings`
- **Purpose**: Track and analyze job postings from various companies
- **Layout**: Custom dashboard with job listings and analytics
- **Features**: Real-time job scraping, company tracking, job alerts

## Adding New Labs

To add a new lab:

1. **Create the lab data** in `src/data/mock.ts`:
   ```typescript
   {
     id: "your-lab-identifier",
     title: "Your Lab Title",
     summary: "Lab description",
     keywords: ["keyword1", "keyword2"],
     // ... other properties
   }
   ```

2. **Create the directory**: `mkdir -p src/app/labs/your-lab-identifier`

3. **Create the page**: `src/app/labs/your-lab-identifier/page.tsx`

4. **Customize the layout**: Each lab can have its own unique layout, components, and functionality

## Lab Identifier Convention

Use descriptive, kebab-case identifiers:
- ✅ `job-postings`
- ✅ `weather-patterns`
- ✅ `stock-analysis`
- ✅ `energy-usage`
- ❌ `lab1`, `lab2` (too generic)
- ❌ `job_postings` (use kebab-case)

## Benefits of This Structure

- **Custom layouts**: Each lab can have completely different UI/UX
- **SEO-friendly**: Descriptive URLs like `/labs/job-postings`
- **Scalable**: Easy to add new labs without affecting existing ones
- **Maintainable**: Each lab is self-contained
- **Flexible**: Can use different data sources, APIs, or components per lab
