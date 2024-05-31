REM Python command NOT working
REM python -m pandoc write va_resume.md -f markdown -t html -c resume-stylesheet.css -s -o output/va_resume.html
REM python -m wkhtmltopdf --enable-local-file-access output/va_resume.html output/va_resume.pdf

REM pandoc if installed through windows:
pandoc va_resume.md -f markdown -t html -c resume-stylesheet.css -s -o output/va_resume.html

REM 
python -m wkhtmltopdf --enable-local-file-access output/va_resume.html output/va_resume.pdf