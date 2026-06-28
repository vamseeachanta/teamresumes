# Career Page - API-centric / firm-first portfolio copy

> **DRAFT - Vamsee publishes manually.** Short portfolio copy for the public career/portfolio
> page, tying the work to live API paths + report URLs. Firm-first per aceengineer-strategy#94.
> Honesty rule: offshore is live proof; CAD/CAM, manufacturing, electrical, safety are
> "onboarding" API paths, never shipped capability. Replace bracketed `[...]` with real links.

---

## Hero

**AceEngineer builds Deckhand - the API for real-world engineering work.**

Every engineering workflow is an API path. One call - `POST /api/run` - returns a **standards-traceable HTML report URL**. Same input, same output, every time. Built on the open-source `digitalmodel` library (7,000+ standard-mapped functions, 42 standards), so every result is deterministic and auditable.

*Offshore is live today. More domains are onboarding.*

[Try a live API call -> report URL] · [See the API catalog] · [aceengineer.com]

---

## How it works (the contract)

```
POST /api/run
  { "ref": "digitalmodel:mooring-fatigue@2",
    "domain": "floating-marine", "subdomain": "mooring", "inputs": {...} }
-> { "status": "PASS",
     "report_url": "https://vamseeachanta.github.io/deckhand-sandbox/.../report.html",
     "artifacts": [...], "duration_s": 12.4 }
```

- **Every workflow is an API path** - cataloged, callable, versioned.
- **Every call returns a deliverable URL** - a report with the governing standard (DNV, API) cited inline.
- **Chat is one client.** Telegram, website buttons, and cron jobs all call the same `/api/run`.

---

## Live API paths (offshore - proven)

| API path | What it returns | Standard |
|---|---|---|
| Mooring fatigue / global analysis | Standards-traceable screening report URL | DNV |
| Subsea-pipeline screening | Deterministic report across hundreds of golden cases | DNV-RP-F105 |
| Installation / umbilical-window analysis | Installation-window report (Yellowtail/Talos lineage) | DNV / API |
| Field-economics screening | BSEE-data analytics over 200+ GoM fields | - |

[View live report examples -> deckhand-sandbox gallery]

## Onboarding (roadmap - not yet shipped)

CAD/CAM · manufacturing · electrical · safety - being onboarded as new API paths. Listed as roadmap, not capability.

---

## The credibility beneath the platform

23+ years of high-consequence offshore engineering - naval architecture, subsea, risers, moorings, installation - for BP, Shell, Chevron, ExxonMobil, ENI, Talos, and others. Engineering Manager for the BP Macondo containment riser response (complete design in 8 weeks). Texas P.E. API-RP-16Q / 17G / 17G2 committee contributor. That track record is why the API can be trusted on real, high-stakes work.

[Full resume] · [LinkedIn] · [GitHub]
