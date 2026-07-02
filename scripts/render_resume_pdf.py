# /// script
# requires-python = ">=3.10"
# dependencies = ["markdown"]
# ///
"""Render cv/va_resume.md to print-ready HTML and PDF via headless Chrome.

Produces two variants:
  cv/va_resume.html + cv/va_resume.pdf          — full contact details (for direct release)
  cv/va_resume_public.pdf                       — PII-scrubbed (published on the Pages site)

Run:  uv run scripts/render_resume_pdf.py
Requires google-chrome (or chromium) on PATH.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CV = ROOT / "cv"
sys.path.insert(0, str(ROOT / "scripts"))
from build_pages import scrub, strip_frontmatter  # noqa: E402

# Embedded print stylesheet (kept in sync with the committed cv/va_resume.html).
CSS = """
@page { size: Letter; margin: 0.55in 0.62in; }
* { box-sizing: border-box; }
body { font-family: Arial, Helvetica, sans-serif; color: #1f2933; font-size: 9.6pt; line-height: 1.28; margin: 0; }
a { color: #0f4c81; text-decoration: none; }
h1 { font-size: 21pt; margin: 0 0 1px; color: #0b1f33; letter-spacing: 0.5px; }
h2 { font-size: 11.5pt; margin: 10px 0 4px; color: #0f4c81; font-weight: 700; page-break-after: avoid; break-after: avoid; }
h1 + h2 { margin: 0 0 8px; color: #0f4c81; font-size: 11.5pt; }
h3 {
  font-size: 10.8pt; margin: 12px 0 2px; color: #0b1f33;
  border-bottom: 1px solid #d5dde5; padding-bottom: 2px;
  page-break-after: avoid; break-after: avoid;
}
p { margin: 4px 0; }
ul { margin: 3px 0 6px; padding-left: 16px; }
li { margin: 0 0 2px; }
hr { border: 0; border-top: 1.5px solid #0f4c81; margin: 8px 0; }
strong { color: #0b1f33; }
.section-break { break-before: page; page-break-before: always; margin-top: 0; }
@media print { h2, h3 { break-after: avoid; page-break-after: avoid; } li { break-inside: avoid; } }
table { border-collapse: collapse; width: 100%; font-size: 8.9pt; margin: 4px 0 6px; }
th { text-align: left; color: #0f4c81; border-bottom: 1.5px solid #0f4c81; padding: 2px 6px 2px 0; }
td { vertical-align: top; border-bottom: 1px solid #e3e9ef; padding: 3px 6px 3px 0; }
td:first-child { white-space: nowrap; }
tr { page-break-inside: avoid; break-inside: avoid; }
h2 { margin: 8px 0 3px; }
li { margin-bottom: 1px; }
"""


def render_html(md_text: str) -> str:
    body = markdown.markdown(strip_frontmatter(md_text), extensions=["tables", "smarty"])
    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        f"<title>Vamsee Achanta CV</title><style>{CSS}</style></head><body>\n{body}\n</body></html>"
    )


def chrome() -> str:
    for name in ("google-chrome", "chromium", "chromium-browser"):
        if shutil.which(name):
            return name
    sys.exit("no Chrome/Chromium found on PATH")


def print_pdf(html_path: Path, pdf_path: Path) -> None:
    subprocess.run(
        [chrome(), "--headless", "--disable-gpu", "--no-sandbox",
         f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer", str(html_path)],
        check=True, capture_output=True,
    )


def main() -> None:
    md_text = (CV / "va_resume.md").read_text(encoding="utf-8")

    full_html = CV / "va_resume.html"
    full_html.write_text(render_html(md_text), encoding="utf-8")
    print_pdf(full_html, CV / "va_resume.pdf")
    print("wrote cv/va_resume.html, cv/va_resume.pdf")

    # Scrubbed variant: temp HTML must live in cv/ so relative logo paths resolve.
    tmp = CV / ".va_resume_public.tmp.html"
    tmp.write_text(render_html(scrub(md_text)), encoding="utf-8")
    try:
        print_pdf(tmp, CV / "va_resume_public.pdf")
    finally:
        tmp.unlink()
    print("wrote cv/va_resume_public.pdf (PII-scrubbed)")


if __name__ == "__main__":
    main()
