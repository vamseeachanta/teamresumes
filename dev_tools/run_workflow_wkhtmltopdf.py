"""Placeholder wkhtmltopdf workflow.

NOTE: This file currently contains only the upstream ``wkhtmltopdf`` library
README example and is NOT a working part of this project. Running it would
generate a PDF of ``http://www.example.com`` into the user's home directory,
which is almost certainly not what you want. The real PDF workflow lives in
``dev_tools/run_workflow_pdfkit.py``.

It is guarded behind ``__main__`` so merely importing this module has no side
effects. Implement the intended workflow (iterate ``cv/*.md`` -> pandoc ->
wkhtmltopdf) before wiring it into the build.
"""


def main() -> None:
    from wkhtmltopdf import WKHtmlToPdf

    wkhtmltopdf = WKHtmlToPdf(
        url='http://www.example.com',
        output_file='~/example.pdf',
    )
    wkhtmltopdf.render()


if __name__ == '__main__':
    raise SystemExit(
        "run_workflow_wkhtmltopdf.py is an unimplemented placeholder; "
        "it would render http://www.example.com to ~/example.pdf. "
        "Implement the cv/*.md -> wkhtmltopdf workflow before running."
    )
