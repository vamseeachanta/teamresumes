#!/usr/bin/env python3
"""
Maintenance Agent - Project Maintenance and Monitoring
Handles dependency monitoring, security scanning, and project health analysis
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DependencyAnalyzer:
    """Analyzes project dependencies and checks for updates/vulnerabilities"""
    
    def __init__(self):
        self.supported_languages = ['python', 'nodejs', 'ruby', 'php']
    
    def analyze_python_dependencies(self, requirements_file: str) -> List[Dict[str, Any]]:
        """Analyze Python dependencies from requirements.txt or similar files"""
        dependencies = []
        
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse package==version format
                if '==' in line:
                    parts = line.split('==')
                    if len(parts) == 2:
                        package_name = parts[0].strip()
                        version = parts[1].strip()
                        
                        dependencies.append({
                            'name': package_name,
                            'version': version,
                            'type': 'python',
                            'file': requirements_file,
                            'line': line_num,
                            'specification': line
                        })
                
                # Parse package>=version format
                elif '>=' in line:
                    parts = line.split('>=')
                    if len(parts) == 2:
                        package_name = parts[0].strip()
                        min_version = parts[1].strip()
                        
                        dependencies.append({
                            'name': package_name,
                            'version': f">={min_version}",
                            'type': 'python',
                            'file': requirements_file,
                            'line': line_num,
                            'specification': line
                        })
                
                # Parse package~=version format (compatible release)
                elif '~=' in line:
                    parts = line.split('~=')
                    if len(parts) == 2:
                        package_name = parts[0].strip()
                        version = parts[1].strip()
                        
                        dependencies.append({
                            'name': package_name,
                            'version': f"~={version}",
                            'type': 'python',
                            'file': requirements_file,
                            'line': line_num,
                            'specification': line
                        })
                
                # Parse package without version
                elif line and not any(op in line for op in ['==', '>=', '<=', '>', '<', '~=', '!=']):
                    dependencies.append({
                        'name': line.strip(),
                        'version': 'latest',
                        'type': 'python',
                        'file': requirements_file,
                        'line': line_num,
                        'specification': line
                    })
        
        except FileNotFoundError:
            logger.error(f"Requirements file not found: {requirements_file}")
        except Exception as e:
            logger.error(f"Error parsing Python dependencies: {e}")
        
        return dependencies
    
    def analyze_nodejs_dependencies(self, package_json_file: str) -> List[Dict[str, Any]]:
        """Analyze Node.js dependencies from package.json"""
        dependencies = []
        
        try:
            with open(package_json_file, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
            
            # Process production dependencies
            for name, version in package_data.get('dependencies', {}).items():
                dependencies.append({
                    'name': name,
                    'version': version,
                    'type': 'nodejs',
                    'category': 'production',
                    'file': package_json_file,
                    'specification': f"{name}@{version}"
                })
            
            # Process development dependencies
            for name, version in package_data.get('devDependencies', {}).items():
                dependencies.append({
                    'name': name,
                    'version': version,
                    'type': 'nodejs',
                    'category': 'development',
                    'file': package_json_file,
                    'specification': f"{name}@{version}"
                })
        
        except FileNotFoundError:
            logger.error(f"Package.json file not found: {package_json_file}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in package.json: {e}")
        except Exception as e:
            logger.error(f"Error parsing Node.js dependencies: {e}")
        
        return dependencies
    
    def check_outdated_dependencies(self, requirements_file: str) -> List[Dict[str, Any]]:
        """Check for outdated Python dependencies using pip list --outdated"""
        outdated_packages = []
        
        try:
            # Get current dependencies
            current_deps = self.analyze_python_dependencies(requirements_file)
            
            # Mock outdated check (in real implementation, would use pip list --outdated)
            for dep in current_deps:
                # Simple heuristic: if version is less than 2.0.0, consider it potentially outdated
                if dep['version'] != 'latest' and '==' in dep['version']:
                    current_version = dep['version'].replace('==', '')
                    try:
                        # Simple version comparison heuristic
                        major_version = int(current_version.split('.')[0])
                        if major_version < 2:
                            # Mock latest version (in real implementation, would query PyPI)
                            latest_version = f"{major_version + 1}.0.0"
                            outdated_packages.append({
                                'name': dep['name'],
                                'current_version': current_version,
                                'latest_version': latest_version,
                                'type': 'python',
                                'severity': 'medium'
                            })
                    except (ValueError, IndexError):
                        # Skip packages with non-standard version formats
                        continue
        
        except Exception as e:
            logger.error(f"Error checking outdated dependencies: {e}")
        
        return outdated_packages
    
    def analyze_dependency_tree(self, project_path: str) -> Dict[str, Any]:
        """Analyze the complete dependency tree for the project"""
        analysis = {
            'python_dependencies': [],
            'nodejs_dependencies': [],
            'total_dependencies': 0,
            'outdated_count': 0,
            'vulnerability_count': 0,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        project_path = Path(project_path)
        
        # Check for Python dependencies
        for req_file in ['requirements.txt', 'Pipfile', 'pyproject.toml']:
            req_path = project_path / req_file
            if req_path.exists():
                deps = self.analyze_python_dependencies(str(req_path))
                analysis['python_dependencies'].extend(deps)
        
        # Check for Node.js dependencies
        package_json_path = project_path / 'package.json'
        if package_json_path.exists():
            deps = self.analyze_nodejs_dependencies(str(package_json_path))
            analysis['nodejs_dependencies'].extend(deps)
        
        # Calculate totals
        analysis['total_dependencies'] = (
            len(analysis['python_dependencies']) + 
            len(analysis['nodejs_dependencies'])
        )
        
        # Check for outdated packages
        if analysis['python_dependencies']:
            req_path = project_path / 'requirements.txt'
            if req_path.exists():
                outdated = self.check_outdated_dependencies(str(req_path))
                analysis['outdated_count'] = len(outdated)
        
        return analysis


class SecurityScanner:
    """Scans for security vulnerabilities and issues"""
    
    def __init__(self):
        self.security_patterns = {
            'hardcoded_secrets': [
                r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?([a-z0-9]{20,})["\']?',
                r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']?([a-z0-9]{20,})["\']?',
                r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?([^"\'\s]{8,})["\']?',
                r'(?i)(token|auth[_-]?token)\s*[=:]\s*["\']?([a-z0-9]{20,})["\']?',
            ],
            'sql_injection': [
                r'(?i)query\s*=.*\+.*user.*input',
                r'(?i)execute\s*\(.*\%.*\)',
                r'(?i)SELECT.*FROM.*WHERE.*\+',
            ],
            'command_injection': [
                r'subprocess\..*shell\s*=\s*True',
                r'os\.system\s*\(',
                r'eval\s*\(',
                r'exec\s*\(',
            ]
        }
    
    def scan_code_security(self, file_path: str) -> List[Dict[str, Any]]:
        """Scan a code file for security issues"""
        security_issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_num, line in enumerate(lines, 1):
                line_content = line.strip()
                
                # Check for various security patterns
                for issue_type, patterns in self.security_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, line_content):
                            security_issues.append({
                                'type': issue_type,
                                'severity': self._get_severity(issue_type),
                                'line': line_num,
                                'content': line_content,
                                'file': file_path,
                                'description': self._get_description(issue_type),
                                'recommendation': self._get_recommendation(issue_type)
                            })
        
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {e}")
        
        return security_issues
    
    def detect_secrets(self, file_path: str) -> List[Dict[str, Any]]:
        """Detect hardcoded secrets in configuration files"""
        secrets = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            secret_patterns = {
                'api_key': r'(?i)(api[_-]?key|apikey)\s*[=:]\s*["\']?([a-z0-9]{20,})["\']?',
                'database_password': r'(?i)(password|passwd)\s*[=:]\s*["\']?([^"\'\s]{8,})["\']?',
                'secret_key': r'(?i)(secret[_-]?key|secretkey)\s*[=:]\s*["\']?([a-z0-9]{20,})["\']?',
                'token': r'(?i)(token|auth[_-]?token)\s*[=:]\s*["\']?([a-z0-9-_]{20,})["\']?',
                'aws_key': r'(?i)(aws[_-]?secret[_-]?access[_-]?key)\s*[=:]\s*["\']?([a-z0-9/+]{40})["\']?',
            }
            
            for line_num, line in enumerate(lines, 1):
                for secret_type, pattern in secret_patterns.items():
                    match = re.search(pattern, line)
                    if match:
                        # Extract the secret value and create preview
                        full_value = match.group(2) if len(match.groups()) >= 2 else match.group(1)
                        value_preview = full_value[:4] + '...' + full_value[-4:] if len(full_value) > 8 else full_value
                        
                        secrets.append({
                            'type': secret_type,
                            'line': line_num,
                            'value_preview': value_preview,
                            'file': file_path,
                            'confidence': 'high' if len(full_value) > 15 else 'medium',
                            'recommendation': 'Move to environment variables or secure vault'
                        })
        
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error detecting secrets in {file_path}: {e}")
        
        return secrets
    
    def check_file_permissions(self, directory_path: str) -> List[Dict[str, Any]]:
        """Check for insecure file permissions"""
        permission_issues = []
        
        try:
            directory_path = Path(directory_path)
            sensitive_files = ['.env', 'config.conf', 'secrets.json', 'private.key']
            
            for file_path in directory_path.rglob('*'):
                if file_path.is_file():
                    # Check if it's a sensitive file
                    if any(sensitive in file_path.name.lower() for sensitive in sensitive_files):
                        try:
                            # Get file permissions (mock implementation)
                            stat_info = file_path.stat()
                            permissions = oct(stat_info.st_mode)[-3:]
                            
                            # Check for overly permissive permissions
                            if permissions.endswith('77') or permissions.endswith('66'):
                                permission_issues.append({
                                    'file': str(file_path),
                                    'current_permissions': permissions,
                                    'recommended_permissions': '600',
                                    'issue': 'File is readable/writable by others',
                                    'severity': 'medium'
                                })
                        except OSError:
                            continue
        
        except Exception as e:
            logger.error(f"Error checking file permissions: {e}")
        
        return permission_issues
    
    def scan_dependencies(self, requirements_file: str) -> Dict[str, Any]:
        """Scan dependencies for known vulnerabilities"""
        vulnerability_report = {
            'scanned_packages': 0,
            'vulnerabilities_found': 0,
            'high_severity': 0,
            'medium_severity': 0,
            'low_severity': 0,
            'scan_timestamp': datetime.now().isoformat(),
            'vulnerabilities': []
        }
        
        try:
            # Analyze dependencies first
            analyzer = DependencyAnalyzer()
            dependencies = analyzer.analyze_python_dependencies(requirements_file)
            vulnerability_report['scanned_packages'] = len(dependencies)
            
            # Mock vulnerability scanning (in real implementation, would use safety, pip-audit, etc.)
            vulnerable_packages = ['requests', 'urllib3', 'jinja2', 'werkzeug', 'flask']
            
            for dep in dependencies:
                if dep['name'].lower() in vulnerable_packages:
                    # Mock vulnerability data
                    vulnerability = {
                        'package': dep['name'],
                        'version': dep['version'],
                        'vulnerability_id': f"CVE-2023-{hash(dep['name']) % 10000:04d}",
                        'severity': 'medium',
                        'description': f"Known vulnerability in {dep['name']}",
                        'recommendation': f"Update {dep['name']} to latest version"
                    }
                    vulnerability_report['vulnerabilities'].append(vulnerability)
                    vulnerability_report['vulnerabilities_found'] += 1
                    vulnerability_report['medium_severity'] += 1
        
        except Exception as e:
            logger.error(f"Error scanning dependencies: {e}")
        
        return vulnerability_report
    
    def _get_severity(self, issue_type: str) -> str:
        """Get severity level for security issue type"""
        severity_map = {
            'hardcoded_secrets': 'high',
            'sql_injection': 'high',
            'command_injection': 'high',
            'insecure_permissions': 'medium',
            'outdated_dependency': 'medium'
        }
        return severity_map.get(issue_type, 'low')
    
    def _get_description(self, issue_type: str) -> str:
        """Get description for security issue type"""
        descriptions = {
            'hardcoded_secrets': 'Hardcoded credentials or API keys found',
            'sql_injection': 'Potential SQL injection vulnerability',
            'command_injection': 'Potential command injection vulnerability',
            'insecure_permissions': 'File has insecure permissions'
        }
        return descriptions.get(issue_type, 'Security issue detected')
    
    def _get_recommendation(self, issue_type: str) -> str:
        """Get recommendation for security issue type"""
        recommendations = {
            'hardcoded_secrets': 'Move secrets to environment variables or secure vault',
            'sql_injection': 'Use parameterized queries or ORM',
            'command_injection': 'Avoid shell=True, validate inputs',
            'insecure_permissions': 'Set appropriate file permissions (600 for sensitive files)'
        }
        return recommendations.get(issue_type, 'Review and fix security issue')


class ProjectHealthMonitor:
    """Monitors overall project health and quality metrics"""
    
    def __init__(self):
        self.health_metrics = {}
    
    def calculate_code_quality_metrics(self, file_path: str) -> Dict[str, Any]:
        """Calculate code quality metrics for a file"""
        metrics = {
            'lines_of_code': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'function_count': 0,
            'class_count': 0,
            'comment_ratio': 0.0,
            'complexity_estimate': 0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line_stripped = line.strip()
                
                if not line_stripped:
                    metrics['blank_lines'] += 1
                elif line_stripped.startswith('#'):
                    metrics['comment_lines'] += 1
                elif '"""' in line_stripped or "'''" in line_stripped:
                    metrics['comment_lines'] += 1
                else:
                    metrics['lines_of_code'] += 1
                    
                    # Count functions and classes
                    if line_stripped.startswith('def '):
                        metrics['function_count'] += 1
                    elif line_stripped.startswith('class '):
                        metrics['class_count'] += 1
                    
                    # Simple complexity indicators
                    if any(keyword in line_stripped for keyword in ['if ', 'for ', 'while ', 'try:', 'except']):
                        metrics['complexity_estimate'] += 1
            
            # Calculate comment ratio
            total_lines = metrics['lines_of_code'] + metrics['comment_lines']
            if total_lines > 0:
                metrics['comment_ratio'] = metrics['comment_lines'] / total_lines
        
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error calculating metrics for {file_path}: {e}")
        
        return metrics
    
    def analyze_test_coverage(self, project_path: str) -> Dict[str, Any]:
        """Analyze test coverage for the project"""
        coverage_analysis = {
            'test_files_found': 0,
            'source_files_found': 0,
            'coverage_estimate': 0.0,
            'test_directories': [],
            'source_directories': [],
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        try:
            project_path = Path(project_path)
            
            # Find test files
            test_patterns = ['test_*.py', '*_test.py', 'tests.py']
            test_files = []
            for pattern in test_patterns:
                test_files.extend(project_path.rglob(pattern))
            
            coverage_analysis['test_files_found'] = len(test_files)
            
            # Find source files (excluding tests)
            source_files = []
            for py_file in project_path.rglob('*.py'):
                if not any(test_pattern.replace('*', '') in py_file.name for test_pattern in ['test_', '_test', 'tests']):
                    source_files.append(py_file)
            
            coverage_analysis['source_files_found'] = len(source_files)
            
            # Simple coverage estimate
            if coverage_analysis['source_files_found'] > 0:
                coverage_analysis['coverage_estimate'] = min(
                    coverage_analysis['test_files_found'] / coverage_analysis['source_files_found'],
                    1.0
                )
            
            # Identify test and source directories
            test_dirs = set()
            source_dirs = set()
            
            for test_file in test_files:
                test_dirs.add(str(test_file.parent))
            
            for source_file in source_files:
                source_dirs.add(str(source_file.parent))
            
            coverage_analysis['test_directories'] = list(test_dirs)
            coverage_analysis['source_directories'] = list(source_dirs)
        
        except Exception as e:
            logger.error(f"Error analyzing test coverage: {e}")
        
        return coverage_analysis
    
    def validate_project_structure(self, project_path: str) -> Dict[str, Any]:
        """Validate standard project structure elements"""
        structure_validation = {
            'has_readme': False,
            'has_requirements': False,
            'has_gitignore': False,
            'has_tests': False,
            'has_docs': False,
            'has_src': False,
            'has_config': False,
            'missing_files': [],
            'recommendations': []
        }
        
        try:
            project_path = Path(project_path)
            
            # Check for standard files
            readme_files = ['README.md', 'README.txt', 'README.rst', 'readme.md']
            for readme in readme_files:
                if (project_path / readme).exists():
                    structure_validation['has_readme'] = True
                    break
            
            requirements_files = ['requirements.txt', 'Pipfile', 'pyproject.toml', 'package.json']
            for req_file in requirements_files:
                if (project_path / req_file).exists():
                    structure_validation['has_requirements'] = True
                    break
            
            if (project_path / '.gitignore').exists():
                structure_validation['has_gitignore'] = True
            
            # Check for directories
            if (project_path / 'tests').exists() or (project_path / 'test').exists():
                structure_validation['has_tests'] = True
            
            if (project_path / 'docs').exists() or (project_path / 'documentation').exists():
                structure_validation['has_docs'] = True
            
            if (project_path / 'src').exists():
                structure_validation['has_src'] = True
            
            config_files = ['config.py', 'settings.py', '.env', 'config.json']
            for config_file in config_files:
                if (project_path / config_file).exists():
                    structure_validation['has_config'] = True
                    break
            
            # Generate recommendations
            if not structure_validation['has_readme']:
                structure_validation['missing_files'].append('README.md')
                structure_validation['recommendations'].append('Add README.md with project description')
            
            if not structure_validation['has_requirements']:
                structure_validation['missing_files'].append('requirements.txt')
                structure_validation['recommendations'].append('Add requirements.txt for dependency management')
            
            if not structure_validation['has_gitignore']:
                structure_validation['missing_files'].append('.gitignore')
                structure_validation['recommendations'].append('Add .gitignore to exclude unwanted files')
            
            if not structure_validation['has_tests']:
                structure_validation['missing_files'].append('tests/')
                structure_validation['recommendations'].append('Add tests directory with unit tests')
        
        except Exception as e:
            logger.error(f"Error validating project structure: {e}")
        
        return structure_validation
    
    def analyze_git_health(self, project_path: str) -> Dict[str, Any]:
        """Analyze git repository health"""
        git_health = {
            'is_git_repo': False,
            'has_remote': False,
            'current_branch': None,
            'branch_count': 0,
            'commit_count': 0,
            'last_commit_date': None,
            'uncommitted_changes': False,
            'branch_info': {},
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        try:
            project_path = Path(project_path)
            git_dir = project_path / '.git'
            
            if git_dir.exists():
                git_health['is_git_repo'] = True
                
                try:
                    # Check current branch
                    result = subprocess.run(
                        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                        cwd=project_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if result.returncode == 0:
                        git_health['current_branch'] = result.stdout.strip()
                    
                    # Check for remote
                    result = subprocess.run(
                        ['git', 'remote'],
                        cwd=project_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        git_health['has_remote'] = True
                    
                    # Check for uncommitted changes
                    result = subprocess.run(
                        ['git', 'status', '--porcelain'],
                        cwd=project_path,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    if result.returncode == 0:
                        git_health['uncommitted_changes'] = bool(result.stdout.strip())
                
                except subprocess.SubprocessError:
                    # Git commands failed, but it's still a git repo
                    pass
        
        except Exception as e:
            logger.error(f"Error analyzing git health: {e}")
        
        return git_health


class MaintenanceReporter:
    """Generates maintenance reports and recommendations"""
    
    def __init__(self):
        self.report_templates = {}
    
    def generate_maintenance_report(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive maintenance report"""
        report = {
            'report_type': 'maintenance',
            'generated_at': datetime.now().isoformat(),
            'summary': {},
            'dependencies': {},
            'security': {},
            'code_quality': {},
            'recommendations': [],
            'action_items': []
        }
        
        try:
            # Process dependencies data
            if 'dependencies' in analysis_data:
                deps = analysis_data['dependencies']
                report['dependencies'] = {
                    'total_packages': len(deps),
                    'outdated_packages': sum(1 for dep in deps if dep.get('outdated', False)),
                    'by_language': self._group_dependencies_by_language(deps)
                }
            
            # Process security data
            if 'security_issues' in analysis_data:
                security_issues = analysis_data['security_issues']
                report['security'] = {
                    'total_issues': len(security_issues),
                    'high_severity': sum(1 for issue in security_issues if issue.get('severity') == 'high'),
                    'medium_severity': sum(1 for issue in security_issues if issue.get('severity') == 'medium'),
                    'low_severity': sum(1 for issue in security_issues if issue.get('severity') == 'low'),
                    'issues_by_type': self._group_security_issues_by_type(security_issues)
                }
            
            # Process code quality data
            if 'code_quality' in analysis_data:
                quality = analysis_data['code_quality']
                report['code_quality'] = {
                    'total_loc': quality.get('lines_of_code', 0),
                    'comment_ratio': quality.get('comment_ratio', 0.0),
                    'function_count': quality.get('function_count', 0),
                    'class_count': quality.get('class_count', 0),
                    'quality_score': self._calculate_quality_score(quality)
                }
            
            # Generate summary
            report['summary'] = self._generate_summary(report)
            
            # Generate recommendations
            report['recommendations'] = self._generate_recommendations(report)
            
        except Exception as e:
            logger.error(f"Error generating maintenance report: {e}")
        
        return report
    
    def prioritize_recommendations(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize recommendations based on severity and impact"""
        recommendations = []
        
        # Priority mapping
        priority_map = {
            'high': 1,
            'medium': 2,
            'low': 3
        }
        
        # Sort issues by severity
        sorted_issues = sorted(issues, key=lambda x: priority_map.get(x.get('severity', 'low'), 3))
        
        for issue in sorted_issues:
            severity = issue.get('severity', 'low')
            issue_type = issue.get('type', 'unknown')
            
            recommendation = {
                'priority': severity,
                'type': issue_type,
                'description': issue.get('description', ''),
                'action': self._get_action_for_issue_type(issue_type),
                'impact': self._get_impact_description(severity),
                'effort': self._estimate_effort(issue_type),
                'timeline': self._suggest_timeline(severity)
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _group_dependencies_by_language(self, dependencies: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group dependencies by programming language"""
        language_counts = {}
        for dep in dependencies:
            lang = dep.get('type', 'unknown')
            language_counts[lang] = language_counts.get(lang, 0) + 1
        return language_counts
    
    def _group_security_issues_by_type(self, security_issues: List[Dict[str, Any]]) -> Dict[str, int]:
        """Group security issues by type"""
        type_counts = {}
        for issue in security_issues:
            issue_type = issue.get('type', 'unknown')
            type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
        return type_counts
    
    def _calculate_quality_score(self, quality_metrics: Dict[str, Any]) -> float:
        """Calculate overall quality score"""
        score = 0.0
        
        # Comment ratio score (0-25 points)
        comment_ratio = quality_metrics.get('comment_ratio', 0.0)
        score += min(comment_ratio * 100, 25)
        
        # Function density score (0-25 points)
        loc = quality_metrics.get('lines_of_code', 1)
        func_count = quality_metrics.get('function_count', 0)
        if loc > 0:
            func_density = func_count / (loc / 100)  # Functions per 100 lines
            score += min(func_density * 5, 25)
        
        # Complexity score (0-25 points) - lower complexity is better
        complexity = quality_metrics.get('complexity_estimate', 0)
        if loc > 0:
            complexity_ratio = complexity / loc
            score += max(25 - complexity_ratio * 1000, 0)
        else:
            score += 25
        
        # Structure score (0-25 points)
        if quality_metrics.get('class_count', 0) > 0:
            score += 15  # Has classes (good structure)
        if quality_metrics.get('function_count', 0) > 0:
            score += 10  # Has functions
        
        return min(score, 100.0)
    
    def _generate_summary(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of the report"""
        summary = {
            'overall_health': 'good',
            'critical_issues': 0,
            'total_recommendations': 0,
            'key_findings': []
        }
        
        # Count critical issues
        security = report.get('security', {})
        critical_issues = security.get('high_severity', 0)
        summary['critical_issues'] = critical_issues
        
        # Determine overall health
        if critical_issues > 0:
            summary['overall_health'] = 'critical'
        elif security.get('medium_severity', 0) > 5:
            summary['overall_health'] = 'needs_attention'
        elif report.get('dependencies', {}).get('outdated_packages', 0) > 10:
            summary['overall_health'] = 'fair'
        
        # Generate key findings
        deps = report.get('dependencies', {})
        if deps.get('outdated_packages', 0) > 0:
            summary['key_findings'].append(f"{deps['outdated_packages']} outdated dependencies found")
        
        if critical_issues > 0:
            summary['key_findings'].append(f"{critical_issues} high-severity security issues detected")
        
        quality = report.get('code_quality', {})
        quality_score = quality.get('quality_score', 0)
        if quality_score < 60:
            summary['key_findings'].append("Code quality score below recommended threshold")
        
        return summary
    
    def _generate_recommendations(self, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Dependency recommendations
        deps = report.get('dependencies', {})
        if deps.get('outdated_packages', 0) > 0:
            recommendations.append({
                'category': 'dependencies',
                'priority': 'medium',
                'title': 'Update outdated dependencies',
                'description': f"Found {deps['outdated_packages']} outdated packages",
                'action': 'Review and update dependencies to latest versions'
            })
        
        # Security recommendations
        security = report.get('security', {})
        if security.get('high_severity', 0) > 0:
            recommendations.append({
                'category': 'security',
                'priority': 'high',
                'title': 'Address critical security issues',
                'description': f"Found {security['high_severity']} high-severity security issues",
                'action': 'Immediately review and fix security vulnerabilities'
            })
        
        # Code quality recommendations
        quality = report.get('code_quality', {})
        quality_score = quality.get('quality_score', 0)
        if quality_score < 70:
            recommendations.append({
                'category': 'code_quality',
                'priority': 'low',
                'title': 'Improve code quality',
                'description': f"Code quality score: {quality_score:.1f}/100",
                'action': 'Add more comments, improve structure, reduce complexity'
            })
        
        return recommendations
    
    def _get_action_for_issue_type(self, issue_type: str) -> str:
        """Get recommended action for issue type"""
        actions = {
            'security': 'Review and fix security vulnerability',
            'dependency': 'Update to latest version',
            'quality': 'Refactor code to improve quality',
            'structure': 'Reorganize project structure',
            'documentation': 'Add or update documentation'
        }
        return actions.get(issue_type, 'Review and address issue')
    
    def _get_impact_description(self, severity: str) -> str:
        """Get impact description for severity level"""
        impacts = {
            'high': 'Critical - immediate action required',
            'medium': 'Moderate - should be addressed soon',
            'low': 'Minor - can be addressed in next maintenance cycle'
        }
        return impacts.get(severity, 'Unknown impact')
    
    def _estimate_effort(self, issue_type: str) -> str:
        """Estimate effort required to fix issue type"""
        efforts = {
            'security': 'medium',
            'dependency': 'low',
            'quality': 'medium',
            'structure': 'high',
            'documentation': 'low'
        }
        return efforts.get(issue_type, 'medium')
    
    def _suggest_timeline(self, severity: str) -> str:
        """Suggest timeline based on severity"""
        timelines = {
            'high': 'within 1 week',
            'medium': 'within 1 month',
            'low': 'within 3 months'
        }
        return timelines.get(severity, 'when convenient')


def main():
    """Main function for testing the maintenance agent"""
    # Test dependency analysis
    analyzer = DependencyAnalyzer()
    print("Testing Dependency Analysis...")
    
    # Test security scanning
    scanner = SecurityScanner()
    print("Testing Security Scanning...")
    
    # Test project health monitoring
    monitor = ProjectHealthMonitor()
    print("Testing Project Health Monitoring...")
    
    # Test reporting
    reporter = MaintenanceReporter()
    print("Testing Maintenance Reporting...")
    
    print("Maintenance Agent testing completed!")


if __name__ == "__main__":
    main()