# Git Workflow for Issue #17 Fix

## Recommended Order: Pull First, Then Push

To avoid merge conflicts and ensure you have the latest code:

### Step 1: Pull Latest from Main
```bash
git pull origin main
```

This ensures you have:
- Any changes that were pushed to main since your last pull
- The latest codebase state
- Avoids merge conflicts when you push

### Step 2: If There Are Conflicts

If `git pull` shows conflicts:
```bash
# Git will tell you which files have conflicts
# Resolve them manually, then:
git add .
git commit -m "Resolve merge conflicts"
```

### Step 3: Add and Commit Your Changes
```bash
# Check what we're adding
git status

# Add all the new documentation and fixes
git add .

# Commit with a descriptive message
git commit -m "Fix #17: Add deployment sync documentation and clarify scheduler configuration

- Add DEPLOYMENT_SYNC.md guide for fixing localhost vs deployed discrepancies
- Add ISSUE_17_FIX.md with step-by-step fix instructions
- Update DEPLOYMENT_CHECKLIST.md with backend redeployment requirements
- Clean up Pinterest references in documentation (not currently active)
- Update scheduler docstring to reflect all active scrapers (Microsoft, RBC, Google)"
```

### Step 4: Push to Main
```bash
git push origin main
```

This will trigger Railway auto-deployment (if configured).

### Step 5: Verify Push Succeeded
- Check GitHub to see your commit is there
- Check Railway Dashboard → Deployments to verify auto-deploy triggered

---

## Alternative: If You Want to Create a Branch First

If you prefer to work on a branch and create a PR:

```bash
# Create and switch to new branch
git checkout -b fix/issue-17-deployment-sync

# Make your commits
git add .
git commit -m "Fix #17: Add deployment sync documentation..."

# Push branch
git push origin fix/issue-17-deployment-sync

# Then create PR on GitHub and merge to main
```

But since this is documentation/fix and you're already assigned to the issue, pushing directly to main is fine too.

---

## What We're Pushing

**New Files:**
- `docs/DEPLOYMENT_SYNC.md` - Comprehensive sync guide
- `docs/ISSUE_17_FIX.md` - Issue-specific fix guide
- `ISSUE_17_COMMENT.md` - Draft comment for GitHub issue
- `GIT_WORKFLOW.md` - This file (can delete after use if you want)

**Modified Files:**
- `docs/DEPLOYMENT_CHECKLIST.md` - Added backend redeployment section
- `backend/job-scraper/app/scheduler.py` - Updated docstring
- `backend/job-scraper/README.md` - Updated company list and cleaned up Pinterest refs
- `backend/job-scraper/scrapers/README.md` - Clarified Pinterest is not active
- `README.md` - Added references to new documentation

---

## Quick Command Sequence

If you want to do it all in one go:

```bash
# Pull latest
git pull origin main

# Check status
git status

# Add everything
git add .

# Commit
git commit -m "Fix #17: Add deployment sync documentation and clarify scheduler configuration"

# Push
git push origin main
```

Done! 🎉

