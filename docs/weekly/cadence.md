# Weekly Career-Update Cadence (for #19)

Keep the three career surfaces — resume (teamresumes), career Pages site, and LinkedIn — current by feeding newly-shipped work into them every week. This is the personal-brand arm of the content→outreach flywheel.

## When

**Friday** (pick/confirm). ~20 minutes, or run the drafting agent and review.

## Source signal — what shipped this week

```bash
# Merged PRs across the ecosystem in the last 7 days
gh search prs --owner vamseeachanta --merged "merged:>=$(date -d '7 days ago' +%F)" \
  --limit 50 --json repository,number,title

# Closed issues, same window (optional)
gh search issues --owner vamseeachanta --state closed "closed:>=$(date -d '7 days ago' +%F)" \
  --limit 50 --json repository,number,title
```

Filter to **public-safe wins** only (exclude private-repo client work: FDAS/ACMA/strategy/personal — see the ecosystem epic vamseeachanta/workspace-hub#3223 data-safety notes).

## Weekly checklist

1. **New live demo / result?** → add/refresh a link on the career Pages site (#16).
2. **Notable shipped work?** → one resume bullet (teamresumes #15), with a link/figure.
3. **One LinkedIn update** → either a profile tweak (Featured/Experience) or a short post draft.
4. Record the week in `docs/weekly/<YYYY-MM-DD>-career-update.md` (proposed changes + a ready-to-post LinkedIn draft). **Publishing stays owner-gated.**

## Automation (optional)

A scheduled cloud agent (`/schedule`) that runs the source-signal queries Friday morning, drafts `docs/weekly/<date>-career-update.md`, and opens it for review. It never posts — it only drafts. Hook to the same public-safe filter.

## Guardrails

- Public-safe only: never surface private-repo client content in a public post or the career site.
- Resumes carry PII — render scrubbed for the public site (see #16).
- Publishing to LinkedIn is owner-executed.
