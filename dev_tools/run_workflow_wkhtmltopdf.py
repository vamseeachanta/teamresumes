from wkhtmltopdf import WKHtmlToPdf

wkhtmltopdf = WKHtmlToPdf(
    url='http://www.example.com',
    output_file='~/example.pdf',
)