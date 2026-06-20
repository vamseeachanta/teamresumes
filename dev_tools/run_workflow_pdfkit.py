"""Render a CV HTML file to PDF using pdfkit.

NOTE: pdfkit requires the ``wkhtmltopdf`` binary to be installed on the system.
On Windows that means installing wkhtmltopdf as a program; on Linux install the
``wkhtmltopdf`` package. Without it, ``pdfkit.from_file`` raises OSError.

Guarded behind ``__main__`` so importing this module has no side effects.
"""

from pathlib import Path

INPUT_HTML = "cv/output/va_resume.html"
OUTPUT_PDF = "cv/output/va_resume.pdf"


def main(input_html: str = INPUT_HTML, output_pdf: str = OUTPUT_PDF) -> None:
    import pdfkit

    # Ensure the output directory exists before writing.
    Path(output_pdf).parent.mkdir(parents=True, exist_ok=True)
    pdfkit.from_file(input_html, output_pdf)


if __name__ == '__main__':
    main()
