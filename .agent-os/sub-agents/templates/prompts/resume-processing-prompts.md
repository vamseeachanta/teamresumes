# Resume Processing Agent Prompt Templates

> Specialized prompts for resume validation, PDF generation QA, and content quality
> Version: 1.0.0
> Created: 2025-07-25

## Quick Analysis Prompt

```
Please analyze the resume file `{file_path}` for:
1. Structure and formatting compliance
2. Professional content quality
3. Skills section organization
4. PDF generation readiness

Provide a summary of issues found and actionable recommendations.
```

## Comprehensive Resume Review

```
Perform a comprehensive analysis of the resume file `{file_path}`:

**Structure Review:**
- Validate required sections (contact, experience, skills, education)
- Check heading hierarchy and formatting consistency
- Verify professional presentation standards

**Content Quality:**
- Assess professional language and tone
- Check achievement quantification and specificity
- Evaluate content completeness and depth

**Skills Analysis:**
- Review skills section organization and categorization
- Validate technical vs soft skills balance
- Check for proper formatting and presentation

**PDF Generation:**
- Verify pandoc and wkhtmltopdf availability
- Check CSS stylesheet presence
- Assess file readiness for conversion

Generate a detailed report with:
- Overall quality score (0-100)
- Categorized issues by severity
- Specific line-by-line recommendations
- PDF generation readiness status
- Priority action items for improvement
```

## Format Validation Only

```
Focus specifically on format validation for `{file_path}`:

Check for:
- Proper markdown structure and syntax
- Consistent heading hierarchy (H1, H2, H3)
- Professional contact information format
- Bullet point consistency
- Section organization and completeness

Report any formatting inconsistencies or structural issues that would impact professional presentation.
```

## Skills Section Optimization

```
Analyze and optimize the skills section in `{file_path}`:

**Current Assessment:**
- Identify all skills mentioned
- Categorize as technical, soft, or other
- Assess organization and presentation

**Recommendations:**
- Suggest optimal categorization structure
- Recommend formatting improvements
- Identify skills that could be better organized
- Suggest additions based on experience section

**Output Format:**
Provide both current state analysis and suggested reorganization with specific formatting examples.
```

## Content Professionalization

```
Review `{file_path}` for professional content quality:

**Language Analysis:**
- Identify unprofessional or casual language
- Check for first-person pronoun usage
- Flag vague or weak terminology

**Achievement Enhancement:**
- Find unquantified achievements
- Suggest specific metrics and numbers
- Recommend stronger action verbs

**Content Depth:**
- Assess section completeness
- Identify areas needing more detail
- Suggest content improvements

Provide specific line-by-line suggestions for enhancing professional tone and impact.
```

## PDF Generation Preparation

```
Prepare `{file_path}` for optimal PDF generation:

**Technical Requirements:**
- Verify pandoc installation and version
- Check wkhtmltopdf availability
- Locate and validate CSS stylesheets

**Content Optimization:**
- Ensure proper markdown syntax
- Check for PDF-unfriendly formatting
- Validate character encoding

**Quality Assurance:**
- Predict potential PDF rendering issues
- Suggest formatting adjustments for print
- Recommend optimal page breaks

Generate a pre-flight checklist and resolve any blockers to PDF generation.
```

## Team Resume Consistency

```
Analyze `{file_path}` for consistency with team resume standards:

**Format Consistency:**
- Compare structure with other team resumes
- Validate against team formatting guidelines
- Check section ordering and naming

**Content Standards:**
- Ensure professional tone consistency
- Verify contact information format
- Validate skills categorization approach

**Brand Alignment:**
- Check for consistent professional presentation
- Ensure team-wide formatting standards
- Validate style guide compliance

Report inconsistencies and provide recommendations for alignment with team standards.
```

## Quick Fix Recommendations

```
Provide immediate, actionable fixes for `{file_path}`:

**High Priority (Fix First):**
- Critical formatting errors
- Missing required sections
- Broken structure or syntax

**Medium Priority (Fix Soon):**
- Professional language improvements
- Contact information formatting
- Skills organization

**Low Priority (Polish):**
- Minor formatting consistency
- Content enhancement opportunities
- Style guide compliance

For each issue, provide the exact text to change and the recommended replacement.
```

## LinkedIn Content Generation Prep

```
Analyze `{file_path}` to prepare content for LinkedIn integration:

**Skills Extraction:**
- Identify all technical skills for LinkedIn skills section
- Categorize skills by relevance and expertise level
- Format for LinkedIn import

**Experience Highlights:**
- Extract key achievements for LinkedIn posts
- Identify quantified accomplishments
- Create shareable professional highlights

**Professional Summary:**
- Distill experience into LinkedIn-ready summary
- Extract key value propositions
- Format for professional networking

Generate content snippets ready for LinkedIn profile updates and professional posts.
```

## Error Detection and Correction

```
Systematically detect and correct errors in `{file_path}`:

**Syntax Errors:**
- Markdown formatting issues
- Broken links or references
- Inconsistent bullet points

**Content Errors:**
- Spelling and grammar issues
- Date format inconsistencies
- Contact information problems

**Structure Errors:**
- Missing or empty sections
- Incorrect heading hierarchy
- Poor organization flow

For each error found, provide:
1. Exact location (line number)
2. Description of the issue
3. Specific correction needed
4. Explanation of why it matters
```

## Variables for Dynamic Prompts

```yaml
# Available variables for prompt customization
variables:
  file_path: "Path to the resume file being analyzed"
  team_standards: "Path to team resume standards file"
  css_stylesheet: "Path to resume CSS stylesheet"
  output_format: "report | json | quick | detailed"
  focus_area: "structure | content | skills | pdf | all"
  severity_filter: "critical | important | minor | all"
  
# Usage examples:
# {file_path} -> "cv/john_smith_resume.md"
# {focus_area} -> "skills"
# {output_format} -> "report"
```

## Integration Prompts

### With Code Quality Agent
```
Coordinate with code quality agent to analyze script files referenced in `{file_path}`:
- Validate any mentioned batch/shell scripts
- Check CSS stylesheet quality
- Ensure build script functionality
```

### With Documentation Agent
```
Work with documentation agent to update project documentation after resume analysis:
- Update README with team member information
- Validate cross-references in documentation
- Ensure resume links are functional
```

### With Content Generation Agent
```
Prepare resume data from `{file_path}` for content generation agent:
- Extract skills for LinkedIn posts
- Identify achievements for social content
- Format experience for professional bios
```

## Custom Workflow Prompts

### Resume Onboarding
```
Guide new team member through resume standardization:
1. Analyze current resume format in `{file_path}`
2. Compare against team standards
3. Generate step-by-step improvement plan
4. Provide template and examples
5. Validate final result
```

### Periodic Review
```
Perform periodic review of `{file_path}` for freshness:
- Check if experience section needs updates
- Validate skills remain current
- Assess content against current market trends
- Suggest improvements and additions
```

### Pre-Client Presentation
```
Prepare `{file_path}` for client presentation:
- Ensure maximum professional quality
- Validate PDF generation will succeed
- Check all formatting is presentation-ready
- Generate quality assurance report
```