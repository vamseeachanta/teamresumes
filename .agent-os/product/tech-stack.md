# Technical Stack

> Last Updated: 2025-01-24
> Version: 1.0.0

## Core Technologies

### Application Framework
- **Framework:** Python Scripts
- **Version:** Python 3.x+
- **Language:** Python + Bash/Batch scripting

### Database
- **Primary:** File System (Markdown files)
- **Version:** N/A
- **ORM:** Direct file I/O

## Document Processing Stack

### Markdown Framework
- **Framework:** Pandoc
- **Version:** Latest stable
- **Build Tool:** pandoc CLI + custom scripts

### Import Strategy
- **Strategy:** Python pip packages
- **Package Manager:** pip + conda
- **Python Version:** 3.x (conda environment)

### Document Conversion
- **Framework:** Pandoc + wkhtmltopdf
- **Version:** Latest stable
- **PostProcessing:** Custom Python scripts

### UI Components
- **Library:** CSS Stylesheet
- **Version:** Custom resume-stylesheet.css
- **Installation:** Local file

## Assets & Media

### Fonts
- **Provider:** System fonts + CSS specification
- **Loading Strategy:** Local system fonts

### Icons
- **Library:** None currently
- **Implementation:** CSS styling

## Infrastructure

### Application Hosting
- **Platform:** Local Development + GitHub
- **Service:** Git repository with GitHub Actions
- **Region:** N/A (local files)

### Database Hosting
- **Provider:** File System
- **Service:** Git version control
- **Backups:** Git history + GitHub remote

### Asset Storage
- **Provider:** Local File System + Git
- **CDN:** None
- **Access:** Direct file access

## Deployment

### CI/CD Pipeline
- **Platform:** GitHub Actions
- **Trigger:** Push to main branch, Pull Requests
- **Tests:** PDF generation verification

### Environments
- **Production:** main branch (GitHub)
- **Staging:** Pull request branches
- **Local Development:** Local file system + batch scripts

## Dependencies

### Python Packages
- **Core:** pandas, matplotlib, scipy
- **Visualization:** plotly, dash
- **Testing:** pytest
- **Code Quality:** black, isort
- **Engineering:** OrcFxAPI, digitalmodel, assetutilities

### System Dependencies
- **Document Processing:** pandoc, wkhtmltopdf
- **Version Control:** git
- **Shell:** bash (Unix) + cmd/PowerShell (Windows)