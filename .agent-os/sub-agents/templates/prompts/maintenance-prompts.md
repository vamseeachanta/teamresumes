# Maintenance Agent Prompt Templates

> Specialized prompts for dependency monitoring, security scanning, and project health analysis
> Version: 1.0.0
> Created: 2025-07-27

## Dependency Analysis

### Python Dependencies Check

```
Analyze Python dependencies in the project `{project_path}`:

**Analysis Requirements:**
- Parse requirements.txt, Pipfile, and pyproject.toml files
- Identify current versions and latest available versions
- Check for security vulnerabilities in dependencies
- Assess license compatibility
- Calculate dependency tree complexity

**Output Format:**
1. **Dependency Summary**
   - Total packages: {count}
   - Outdated packages: {count}
   - Vulnerable packages: {count}

2. **Critical Issues**
   - List packages with known vulnerabilities
   - Highlight breaking changes in updates
   - Flag deprecated packages

3. **Recommendations**
   - Priority updates with risk assessment
   - Safe upgrade paths
   - Alternative package suggestions

**Focus Areas:**
- Security vulnerabilities (CVEs)
- Maintenance status of packages
- Version compatibility matrix
- Performance impact of updates
```

### Node.js Dependencies Audit

```
Perform comprehensive Node.js dependency audit for `{project_path}`:

**Audit Scope:**
- Analyze package.json and package-lock.json
- Check npm audit results
- Evaluate development vs production dependencies
- Assess bundle size impact
- Review peer dependency conflicts

**Security Assessment:**
- Scan for known vulnerabilities
- Check for malicious packages
- Validate package authenticity
- Review download statistics and maintainer activity

**Performance Analysis:**
- Bundle size impact analysis
- Load time implications
- Tree-shaking compatibility
- Alternative lightweight packages

**Report Structure:**
- Executive summary with risk scores
- Detailed vulnerability breakdown
- Upgrade recommendations with testing notes
- Long-term maintenance strategy
```

### Dependency Update Strategy

```
Create dependency update strategy for `{project_path}`:

**Strategy Components:**
1. **Risk Assessment Matrix**
   - Critical security updates (immediate)
   - Major version updates (planned)
   - Minor/patch updates (automated)

2. **Update Prioritization**
   - Security patches: immediate deployment
   - Feature updates: next sprint cycle
   - Major upgrades: quarterly planning

3. **Testing Requirements**
   - Automated test coverage for updates
   - Compatibility testing procedures
   - Rollback plans for failed updates

4. **Monitoring Setup**
   - Dependency vulnerability alerts
   - Automated update notifications
   - Health check dashboards

**Timeline Recommendations:**
- Weekly: Security patch reviews
- Monthly: Minor update cycles
- Quarterly: Major version planning
- Annually: Dependency stack review
```

## Security Scanning

### Code Security Analysis

```
Perform comprehensive security analysis on `{file_path}`:

**Security Scan Areas:**
1. **Static Code Analysis**
   - Hardcoded secrets detection
   - SQL injection patterns
   - Command injection vulnerabilities
   - Cross-site scripting (XSS) risks
   - Insecure cryptographic implementations

2. **Configuration Security**
   - Environment variable usage
   - File permissions audit
   - Database connection security
   - API endpoint protection

3. **Dependency Security**
   - Known vulnerability scanning
   - Outdated security patches
   - Malicious package detection
   - License compliance issues

**Report Format:**
- **Critical Issues** (immediate action required)
- **High Priority** (address within 1 week)
- **Medium Priority** (address within 1 month)
- **Low Priority** (address in next maintenance cycle)

**Include for each issue:**
- Vulnerability description
- Impact assessment
- Remediation steps
- Code examples of fixes
```

### Secrets Detection Audit

```
Scan for exposed secrets and credentials in `{project_path}`:

**Detection Patterns:**
- API keys and tokens
- Database credentials
- Private keys and certificates
- OAuth secrets
- Third-party service credentials
- Internal system passwords

**Scan Locations:**
- Source code files (.py, .js, .ts, .java, etc.)
- Configuration files (.env, .config, .ini)
- Documentation files (.md, .txt)
- Version control history (git)
- Container images and scripts

**Risk Assessment:**
- **Critical**: Production credentials in public repos
- **High**: API keys with broad permissions
- **Medium**: Development credentials
- **Low**: Test/demo credentials

**Remediation Guide:**
1. Immediate: Rotate exposed credentials
2. Secure: Move to environment variables
3. Implement: Secret management system
4. Monitor: Ongoing secret scanning
```

### Security Compliance Check

```
Evaluate security compliance for project `{project_path}`:

**Compliance Frameworks:**
- OWASP Top 10 vulnerability assessment
- CWE (Common Weakness Enumeration) mapping
- NIST Cybersecurity Framework alignment
- Industry-specific requirements

**Assessment Areas:**
1. **Authentication & Authorization**
   - Password policies
   - Multi-factor authentication
   - Session management
   - Access control implementation

2. **Data Protection**
   - Encryption at rest and in transit
   - Data classification
   - Privacy controls
   - Backup security

3. **Monitoring & Logging**
   - Security event logging
   - Audit trail completeness
   - Incident response procedures
   - Vulnerability management

**Deliverables:**
- Compliance gap analysis
- Risk register with mitigation plans
- Security roadmap with timelines
- Policy and procedure recommendations
```

## Project Health Monitoring

### Code Quality Assessment

```
Assess code quality and maintainability for `{project_path}`:

**Quality Metrics:**
1. **Code Structure**
   - Lines of code analysis
   - Function/class complexity
   - Cyclomatic complexity
   - Code duplication assessment

2. **Documentation Quality**
   - Comment ratio and quality
   - API documentation completeness
   - README and setup instructions
   - Code example availability

3. **Testing Coverage**
   - Unit test coverage percentage
   - Integration test completeness
   - Test quality assessment
   - CI/CD pipeline validation

4. **Maintainability Factors**
   - Code organization patterns
   - Naming convention adherence
   - Dependency management
   - Technical debt indicators

**Scoring System:**
- Excellent (90-100): Production-ready, minimal issues
- Good (70-89): Solid foundation, minor improvements needed
- Fair (50-69): Acceptable, moderate refactoring required
- Poor (<50): Significant improvements needed

**Improvement Recommendations:**
- High-impact, low-effort improvements
- Refactoring priorities
- Documentation gaps
- Testing strategy enhancements
```

### Project Structure Validation

```
Validate project structure and organization for `{project_path}`:

**Structure Assessment:**
1. **Standard Files Checklist**
   - README.md with clear description
   - Requirements/dependencies file
   - .gitignore with appropriate exclusions
   - License file
   - Contributing guidelines

2. **Directory Organization**
   - Source code organization
   - Test directory structure
   - Documentation placement
   - Configuration file management
   - Asset and resource organization

3. **Development Workflow**
   - Branch management strategy
   - Commit message conventions
   - Pull request templates
   - Issue tracking setup
   - Release management process

**Best Practices Evaluation:**
- Language-specific conventions
- Framework recommendations
- Industry standards compliance
- Team collaboration tools

**Recommendations:**
- Missing files and directories
- Reorganization suggestions
- Workflow improvements
- Tool integration opportunities
```

### Performance Health Check

```
Evaluate performance characteristics of `{project_path}`:

**Performance Analysis:**
1. **Code Performance**
   - Algorithm efficiency analysis
   - Memory usage patterns
   - I/O operation optimization
   - Database query performance

2. **Build and Deploy Performance**
   - Build time analysis
   - Bundle size optimization
   - Deployment speed metrics
   - CI/CD pipeline efficiency

3. **Runtime Performance**
   - Application startup time
   - Response time analysis
   - Resource utilization
   - Scalability considerations

**Monitoring Setup:**
- Performance metric collection
- Alerting thresholds
- Benchmarking procedures
- Regression testing

**Optimization Recommendations:**
- Quick wins for immediate improvement
- Long-term performance strategy
- Infrastructure considerations
- Tool and library recommendations
```

## Maintenance Reporting

### Comprehensive Health Report

```
Generate comprehensive maintenance report for `{project_path}`:

**Executive Summary:**
- Overall project health score
- Critical issues requiring immediate attention
- Key achievements and improvements
- Strategic recommendations

**Detailed Analysis:**
1. **Dependencies Health**
   - Package inventory and status
   - Security vulnerability summary
   - Update recommendations with risk assessment
   - License compliance status

2. **Security Posture**
   - Vulnerability scan results
   - Threat model assessment
   - Security control effectiveness
   - Incident response readiness

3. **Code Quality Metrics**
   - Maintainability index
   - Technical debt assessment
   - Test coverage analysis
   - Documentation quality score

4. **Operational Health**
   - CI/CD pipeline status
   - Deployment success rates
   - Monitoring and alerting coverage
   - Backup and recovery procedures

**Action Plan:**
- Immediate actions (next 1-2 weeks)
- Short-term improvements (next 1-3 months)
- Long-term strategic initiatives (6-12 months)
- Resource requirements and timeline
```

### Security Audit Report

```
Create detailed security audit report for `{project_path}`:

**Audit Scope and Methodology:**
- Assessment timeline and coverage
- Tools and techniques used
- Testing approach and limitations
- Compliance framework reference

**Findings Summary:**
- Total vulnerabilities by severity
- Risk assessment matrix
- Trend analysis vs previous audits
- Industry benchmark comparison

**Detailed Findings:**
For each vulnerability:
- **Vulnerability ID**: Unique identifier
- **Severity Level**: Critical/High/Medium/Low
- **Description**: Clear explanation of the issue
- **Impact Assessment**: Business and technical impact
- **Proof of Concept**: Demonstration (if applicable)
- **Remediation**: Step-by-step fix instructions
- **Timeline**: Recommended resolution timeframe

**Remediation Roadmap:**
1. **Critical Issues** (0-7 days)
   - Immediate security patches
   - Temporary mitigations
   - Emergency response procedures

2. **High Priority** (1-4 weeks)
   - Security improvements
   - Configuration hardening
   - Access control enhancements

3. **Medium/Low Priority** (1-6 months)
   - Process improvements
   - Security awareness training
   - Long-term security investments
```

### Dependency Health Dashboard

```
Create dependency health dashboard for `{project_path}`:

**Dashboard Metrics:**
1. **Health Overview**
   - Total dependencies: {count}
   - Up-to-date: {percentage}
   - Security issues: {count}
   - License conflicts: {count}

2. **Risk Assessment**
   - Critical vulnerabilities: {count}
   - High-risk packages: {list}
   - Deprecated dependencies: {count}
   - Maintenance status: {assessment}

3. **Update Recommendations**
   - Safe updates available: {count}
   - Breaking changes: {count}
   - Estimated update effort: {hours}
   - Success probability: {percentage}

**Trending Analysis:**
- Dependency growth over time
- Vulnerability discovery trends
- Update adoption rates
- Security posture improvements

**Actionable Insights:**
- Next recommended update
- Risk reduction opportunities
- Alternative package suggestions
- Long-term dependency strategy
```

## Integration Prompts

### Coordination with Code Quality Agent

```
Coordinate maintenance analysis with code quality agent for `{project_path}`:

**Shared Analysis Areas:**
- Code complexity metrics correlation
- Test coverage impact on maintenance
- Documentation quality assessment
- Refactoring opportunity identification

**Maintenance-Specific Focus:**
- Technical debt quantification
- Update impact on code quality
- Security improvements vs code complexity
- Long-term maintainability planning

**Quality Enhancement Integration:**
- Code review checklist updates
- Automated quality gate configuration
- Maintenance-aware coding standards
- Quality metric tracking for maintenance decisions
```

### Security Framework Integration

```
Integrate maintenance findings with security framework:

**Security-Maintenance Alignment:**
- Vulnerability remediation planning
- Security update prioritization
- Risk-based maintenance scheduling
- Compliance requirement mapping

**Automated Security Maintenance:**
- Security patch automation rules
- Vulnerability scanning integration
- Security metric tracking
- Incident response coordination

**Governance Integration:**
- Security policy compliance checking
- Risk tolerance alignment
- Approval workflow integration
- Audit trail maintenance
```

## Automation and Monitoring

### Automated Health Checks

```
Set up automated health monitoring for `{project_path}`:

**Daily Checks:**
- Security vulnerability scans
- Dependency update availability
- Build and test status
- Performance metric collection

**Weekly Assessments:**
- Code quality trend analysis
- Documentation completeness review
- Test coverage evolution
- Dependency health assessment

**Monthly Reviews:**
- Comprehensive security audit
- Technical debt assessment
- Architecture health evaluation
- Strategic maintenance planning

**Alert Configurations:**
- Critical security vulnerabilities (immediate)
- Build failures (15 minutes)
- Performance degradation (1 hour)
- Test coverage drops (daily)

**Dashboard Updates:**
- Real-time health indicators
- Trend visualization
- Comparison with baselines
- Predictive maintenance alerts
```

### Continuous Maintenance Strategy

```
Implement continuous maintenance strategy for `{project_path}`:

**Maintenance Automation:**
1. **Automated Updates**
   - Security patch auto-application
   - Minor version update scheduling
   - Dependency conflict resolution
   - Rollback procedures

2. **Quality Monitoring**
   - Code quality trend tracking
   - Performance regression detection
   - Documentation drift monitoring
   - Test coverage maintenance

3. **Security Continuous Monitoring**
   - Real-time vulnerability scanning
   - Configuration drift detection
   - Access pattern anomaly detection
   - Compliance monitoring

**Human-in-the-Loop Elements:**
- Major version update approval
- Architecture change decisions
- Security incident response
- Strategic planning and review

**Success Metrics:**
- Mean time to patch (MTTP)
- Security vulnerability exposure time
- Code quality trend direction
- Maintenance cost optimization
```

## Variables for Dynamic Prompts

```yaml
# Available variables for prompt customization
variables:
  project_path: "Path to the project directory being analyzed"
  file_path: "Specific file path for focused analysis"
  analysis_type: "dependency | security | quality | health"
  severity_filter: "critical | high | medium | low | all"
  timeframe: "daily | weekly | monthly | quarterly"
  compliance_framework: "owasp | nist | pci | hipaa | custom"
  
# Usage examples:
# {project_path} -> "/path/to/teamresumes"
# {analysis_type} -> "security"
# {severity_filter} -> "high"
```

## Quality Assurance Prompts

### Maintenance Report Review

```
Review maintenance analysis results for accuracy and completeness:

**Validation Checklist:**
- All critical dependencies identified
- Security findings properly classified
- Risk assessments are realistic
- Recommendations are actionable
- Timeline estimates are reasonable

**Quality Metrics:**
- False positive rate < 5%
- Coverage completeness > 95%
- Actionability score > 80%
- Risk assessment accuracy

**Report Enhancement:**
- Clear executive summary
- Technical details for developers
- Business impact for stakeholders
- Cost-benefit analysis for improvements
```