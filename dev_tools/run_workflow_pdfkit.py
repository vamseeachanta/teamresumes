# Not working as pdfkit requires wkhtmltopdf installed as windows program
import pdfkit

pdfkit.from_file('cv/output/va_resume.html', 'cv/output/va_resume.pdf')
