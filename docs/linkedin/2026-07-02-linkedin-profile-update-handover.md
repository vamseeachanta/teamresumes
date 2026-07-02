# Handover: apply CV-aligned profile to LinkedIn via Claude in Chrome

**Date:** 2026-07-02 · **Issue:** #17 (epic #14) · **Status:** READY TO EXECUTE — blocked
on this machine only because the Claude Chrome extension would not connect (ace-linux;
extension enabled but never paired despite restart guidance). Execute from any computer
where Claude in Chrome works and LinkedIn is logged in as **vamseeachanta**.

## What already shipped (this session, all merged to main)

| PR | What |
|---|---|
| #23 | CV restructured — positions-first page 1, project detail pages 2+ |
| #24 | Employer logo strip on CV page 1 (ACMA/FDAS/AceEngineer/Oxy/2H) |
| #25 | Release PDFs (`cv/va_resume.pdf` full-contact; scrubbed PDF on site) + `scripts/render_resume_pdf.py` |
| #26 | Ecosystem additions — Deckhand, CFD, floating wind, HSE analytics, quantified digitalmodel |
| #27 | **`cv/linkedin/profile-cv-aligned.md` — the LinkedIn source of truth (SSOT)** |

Career site live: <https://vamseeachanta.github.io/teamresumes/> (resume + PDF).
GitHub Pages for this repo was enabled this session — deploys run on every push to main.

## The task remaining

Update the live LinkedIn profile (`linkedin.com/in/vamseeachanta`) **section by section**
to match the SSOT exactly. SSOT (always read the current main version):

    https://raw.githubusercontent.com/vamseeachanta/teamresumes/main/cv/linkedin/profile-cv-aligned.md

Sections, in order: Headline → About → Featured (3 links) → Experience (5 entries) →
Education → Licenses & Certifications → Publications → Skills (20, ordered) →
Organizations. Character limits pre-verified: headline 217/220, About 2,045/2,600;
experience descriptions are all well under LinkedIn's 2,000/role.

## Handover prompt (paste into Claude Code on the executing computer)

```text
Update my live LinkedIn profile to match the repo source of truth, using Claude in
Chrome. I explicitly authorize you to edit and save my LinkedIn profile sections.

Source of truth (SSOT) — fetch the current version, do not work from memory:
https://raw.githubusercontent.com/vamseeachanta/teamresumes/main/cv/linkedin/profile-cv-aligned.md
Context doc: docs/linkedin/2026-07-02-linkedin-profile-update-handover.md in
github.com/vamseeachanta/teamresumes.

Method:
1. Verify the Chrome extension is connected (tabs_context). Create a new tab, go to
   linkedin.com/in/vamseeachanta, confirm I am logged in as vamseeachanta (profile
   shows "Edit" pencils). If not logged in, stop and tell me — never enter credentials.
2. For each section in SSOT order (Headline, About, Featured, each of the 5 Experience
   entries, Education, Licenses, Publications, Skills, Organizations):
   a. Screenshot the section BEFORE editing (rollback reference).
   b. Open its edit dialog, select-all and replace the text with the SSOT text
      VERBATIM (plain text; bullets as "- " or "•"; no markdown ** or #).
   c. Watch the field's character counter; SSOT is pre-sized (headline 217/220,
      About 2045/2600) — if anything still overflows, trim trailing detail, never
      the numbers/claims, and note the trim in your report.
   d. Save, screenshot AFTER, move on.
3. Experience entries: match titles, org names, and date ranges exactly as in SSOT
   (Dec 2023– ACMA / Jun 2016– FDAS / Jun 2012– AceEngineer / Sep 2017–Dec 2020 Oxy /
   Aug 2003–Jun 2015 2H). Do not delete any existing entry that SSOT doesn't cover —
   flag extras in your report instead.
4. Skills: add any of the 20 SSOT skills that are missing; reorder top skills to match
   if LinkedIn allows pinning top 3-5. Do not remove existing endorsed skills — report.
5. Featured: add the 3 SSOT links (career site, Deckhand gallery, digitalmodel
   capabilities) as link items.

Guardrails:
- Touch ONLY profile sections. No posts, no messages, no connection requests, no
  settings, no notifications.
- If LinkedIn shows a verification challenge or captcha: STOP and hand back to me.
- If a live section contains material not in SSOT that looks deliberate (e.g., media
  attachments, recommendations), leave it and flag it.
- If a save fails twice, skip the section and report.

Afterwards:
- Give me a per-section report: changed / unchanged / flagged, with the before/after
  screenshots.
- If any live text had to deviate from SSOT (limits, LinkedIn field quirks), update
  cv/linkedin/profile-cv-aligned.md to match what was actually published and open a
  PR to teamresumes so the SSOT stays true (merge once CI is green — standing
  authorization).
- Comment the outcome on teamresumes issue #17.
```

## Notes for the executing session

- **Voice decision (settled):** engineer-first, matching `cv/va_resume.md`. The
  founder-first draft `cv/linkedin/profile-api-centric.md` is the deliberate
  alternative — do not blend them.
- **Honesty rule:** only shipped work is claimed (offshore live proof, Deckhand,
  digitalmodel, worldenergydata, validated CFD). CAD/CAM, manufacturing, electrical,
  safety are onboarding paths — never "delivered". The old "7,000+ functions / 42
  standards" claim is unverified — SSOT deliberately dropped it; do not reintroduce.
- **Maintenance model (user directive):** LinkedIn is maintained via this repo +
  stable live links (Pages roots that don't change as work improves). Browser-driven
  LinkedIn *review* was judged resource-wasteful; the browser is used only to *apply*
  the SSOT, then everything routes through git again.
