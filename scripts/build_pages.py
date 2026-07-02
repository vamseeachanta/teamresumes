# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build a static career/portfolio GitHub Pages site for teamresumes.

Reuses the deterministic static-site pattern from worldenergydata: a stdlib-only
generator renders source Markdown to static HTML with no server and no API key.

PRIVACY: the public site renders a PII-SCRUBBED resume (email/phone/precise
location removed; LinkedIn/GitHub kept). The source `cv/*.md` is unchanged — only
the rendered HTML is scrubbed. Built `public/` is gitignored and regenerated in CI.

Run:  python3 scripts/build_pages.py   (writes public/)
"""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CV = ROOT / "cv"
PUBLIC = ROOT / "public"
ASSETS = PUBLIC / "assets"

# The one resume rendered publicly (owner-consented). Others stay private until consent.
PUBLIC_RESUME = "va_resume.md"

HEADLINE = "Offshore & Subsea Engineering Leader | Founder, AceEngineer | Building AI-Augmented Engineering Workflows"

DEMOS = [
    ("worldenergydata — live", "https://vamseeachanta.github.io/worldenergydata/",
     "Deterministic Gulf of Mexico field economics & well analytics on public BSEE data: Lower-Tertiary NPVs, 56-well benchmarking, interactive 3D well paths."),
    ("digitalmodel", "https://github.com/vamseeachanta/digitalmodel",
     "Open offshore engineering library — OrcaWave/AQWA hydrodynamic benchmarks, 221 S-N fatigue curves across 17 standards, subsea/riser/cathodic-protection analysis."),
    ("Raw-to-Knowledge Playbook", "https://github.com/vamseeachanta/raw-to-knowledge-playbook",
     "Field-tested methodology for turning raw engineering data into trustworthy, AI-ready knowledge."),
]

# ---------------------------------------------------------------------------
# PII scrub — applied to the rendered resume only.
# ---------------------------------------------------------------------------
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_PHONE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)")


def scrub(md: str) -> str:
    """Remove email/phone and the explicit Email:/Phone: contact labels.
    Keep LinkedIn/GitHub links and city-level location."""
    # Drop a leading "**Email:** ... | **Phone:** ..." line entirely.
    lines = []
    for line in md.splitlines():
        if re.search(r"\*\*Email:\*\*|\*\*Phone:\*\*", line):
            continue
        line = _EMAIL.sub("[contact via LinkedIn]", line)
        line = _PHONE.sub("", line)
        lines.append(line)
    return "\n".join(lines)


def strip_frontmatter(md: str) -> str:
    if md.startswith("---"):
        end = md.find("\n---", 3)
        if end != -1:
            nl = md.find("\n", end + 1)
            return md[nl + 1:] if nl != -1 else ""
    return md


# ---------------------------------------------------------------------------
# Minimal Markdown -> HTML (ATX headings, lists, tables, hr, bold, links,
# inline code). Raw HTML like <br> passes through untouched.
# ---------------------------------------------------------------------------
_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_CODE = re.compile(r"`([^`]+)`")


def _inline(text: str) -> str:
    text = _CODE.sub(lambda m: f"<code>{html.escape(m.group(1))}</code>", text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _LINK.sub(r'<a href="\2">\1</a>', text)
    return text


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i, n = 0, len(lines)
    para: list[str] = []

    def flush():
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para.clear()

    while i < n:
        s = lines[i].strip()
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            flush()
            block = [lines[i], lines[i + 1]]
            i += 2
            while i < n and lines[i].strip().startswith("|"):
                block.append(lines[i]); i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in block]
            head, _al, *body = cells
            t = ["<div class='table-wrap'><table><thead><tr>"]
            t += [f"<th>{_inline(c)}</th>" for c in head] + ["</tr></thead><tbody>"]
            for row in body:
                t.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in row) + "</tr>")
            out.append("".join(t) + "</tbody></table></div>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            flush(); lvl = len(m.group(1))
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if s in ("---", "***", "___"):
            flush(); out.append("<hr>"); i += 1; continue
        if re.match(r"^[-*]\s+", s):
            flush(); items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip())); i += 1
            out.append("<ul>" + "".join(f"<li>{_inline(it)}</li>" for it in items) + "</ul>")
            continue
        if not s:
            flush(); i += 1; continue
        para.append(s); i += 1
    flush()
    return "\n".join(out)


STYLE = """:root{--fg:#1a2230;--muted:#5b6675;--bg:#f7f8fa;--card:#fff;--line:#e2e6ec;--brand:#0f4c81}
*{box-sizing:border-box}
body{margin:0;font:16px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
header.site,footer.site{padding:14px 22px;background:var(--card);border-bottom:1px solid var(--line)}
footer.site{border-top:1px solid var(--line);border-bottom:0;color:var(--muted);font-size:14px;margin-top:48px}
.home{color:var(--brand);text-decoration:none;font-weight:700}
main{max-width:900px;margin:0 auto;padding:28px 22px}
.hero{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:28px;display:flex;gap:24px;align-items:center;flex-wrap:wrap}
.photo{width:120px;height:120px;border-radius:50%;background:#dde3ea;display:flex;align-items:center;justify-content:center;color:var(--muted);font-size:13px;text-align:center;flex:0 0 auto}
.hero h1{margin:.1em 0;font-size:26px}
.headline{color:var(--brand);font-weight:600;margin:.2em 0}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin:26px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;text-decoration:none;color:inherit;transition:.15s;display:block}
.card:hover{border-color:var(--brand);box-shadow:0 4px 16px rgba(15,76,129,.12);transform:translateY(-2px)}
.card h3{margin:.1em 0 .4em;color:var(--brand)}
.card p{color:var(--muted);font-size:14px;margin:0}
.content h2{margin-top:1.6em;border-bottom:1px solid var(--line);padding-bottom:.2em}
.content h3{margin-top:1.3em}
.table-wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{border:1px solid var(--line);padding:6px 10px;text-align:left}
a{color:var(--brand)}
hr{border:0;border-top:1px solid var(--line);margin:1.4em 0}
.note{background:#fff8ec;border:1px solid #f1ddb3;border-radius:8px;padding:10px 14px;font-size:13px;color:#8a5a00;margin:14px 0}
"""


def shell(title: str, body: str, *, home=True) -> str:
    nav = '<a class="home" href="index.html">&larr; Vamsee Achanta</a>' if home else '<span class="home">Vamsee Achanta, P.E.</span>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title><link rel="stylesheet" href="assets/style.css"></head>
<body><header class="site">{nav}</header><main>{body}</main>
<footer class="site"><p>Built as a deterministic static site (no server, no tracking). Source: github.com/vamseeachanta/teamresumes.</p></footer>
</body></html>"""


def build():
    PUBLIC.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "style.css").write_text(STYLE, encoding="utf-8")

    # Static image assets referenced by the resume (e.g. employer logos).
    logos_src = CV / "assets" / "logos"
    if logos_src.is_dir():
        logos_dst = ASSETS / "logos"
        logos_dst.mkdir(exist_ok=True)
        for f in logos_src.iterdir():
            if f.is_file():
                logos_dst.joinpath(f.name).write_bytes(f.read_bytes())

    # Downloadable PDF (PII-scrubbed variant, built by scripts/render_resume_pdf.py)
    pdf_src = CV / "va_resume_public.pdf"
    has_pdf = pdf_src.exists()
    if has_pdf:
        (PUBLIC / "va_resume.pdf").write_bytes(pdf_src.read_bytes())

    # Resume page (scrubbed)
    resume_md = CV / PUBLIC_RESUME
    has_resume = resume_md.exists()
    if has_resume:
        body = md_to_html(strip_frontmatter(scrub(resume_md.read_text(encoding="utf-8"))))
        pdf_link = ' <a href="va_resume.pdf">Download as PDF</a>.' if has_pdf else ""
        (PUBLIC / "resume.html").write_text(shell(
            "Vamsee Achanta — Resume",
            '<div class="note">Public resume: direct contact details removed by design. '
            f'Reach out via <a href="https://www.linkedin.com/in/vamseeachanta">LinkedIn</a>.{pdf_link}</div>'
            f'<div class="content">{body}</div>',
        ), encoding="utf-8")

    # Landing / portfolio
    cards = "".join(
        f'<a class="card" href="{url}"><h3>{html.escape(name)} &rarr;</h3><p>{html.escape(desc)}</p></a>'
        for name, url, desc in DEMOS
    )
    pdf_suffix = ' &middot; <a href="va_resume.pdf">PDF</a>' if has_pdf else ""
    resume_link = f'<p><a href="resume.html">Full resume &rarr;</a>{pdf_suffix}</p>' if has_resume else ""
    landing = shell("Vamsee Achanta, P.E. — Offshore & Subsea Engineering + AI", f"""
<section class="hero">
  <div class="photo">photo<br>placeholder</div>
  <div>
    <h1>Vamsee Achanta, P.E.</h1>
    <p class="headline">{html.escape(HEADLINE)}</p>
    <p>23+ years across the offshore lifecycle — risers, pipelines, moorings, FPSOs, to 6,000 ft —
    now building deterministic, AI-augmented engineering tools and putting the work in the open.</p>
    {resume_link}
  </div>
</section>
<h2>Live work</h2>
<div class="cards">{cards}</div>
<h2>How this site works</h2>
<p>Static HTML, no server, no tracking. The resume renders from Markdown with contact
details scrubbed; the live-work links go to deterministic, unit-tested tools where every
number is shown with its provenance.</p>
""", home=False)
    (PUBLIC / "index.html").write_text(landing, encoding="utf-8")

    pages = sorted(p.name for p in PUBLIC.glob("*.html"))
    print(f"Built {len(pages)} pages: {', '.join(pages)} (resume {'included' if has_resume else 'MISSING'})")


if __name__ == "__main__":
    build()
