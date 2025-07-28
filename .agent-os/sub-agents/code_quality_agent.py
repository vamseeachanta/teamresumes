#!/usr/bin/env python3
"""
Code Quality Agent Implementation
Analyzes code quality, enforces formatting standards, and suggests improvements
"""

import ast
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodeIssue:
    """Represents a code quality issue"""
    
    def __init__(self, file_path: str, line_number: int, severity: str, 
                 issue_type: str, message: str, suggestion: str = ""):
        self.file_path = file_path
        self.line_number = line_number
        self.severity = severity  # critical, important, minor
        self.issue_type = issue_type
        self.message = message
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'file_path': self.file_path,
            'line_number': self.line_number,
            'severity': self.severity,
            'type': self.issue_type,
            'message': self.message,
            'suggestion': self.suggestion
        }


class PythonAnalyzer:
    """Analyzes Python code for quality issues"""
    
    def __init__(self):
        self.issues = []
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a Python file for quality issues"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file is empty
            if not content.strip():
                self.issues.append(CodeIssue(
                    file_path, 1, "minor", "empty_file",
                    "File is empty or contains only whitespace",
                    "Add meaningful content or remove the file"
                ))
                return [issue.to_dict() for issue in self.issues]
            
            # Parse the AST
            try:
                tree = ast.parse(content, filename=file_path)
                self._analyze_ast(tree, file_path, content.split('\n'))
            except SyntaxError as e:
                self.issues.append(CodeIssue(
                    file_path, e.lineno or 1, "critical", "syntax_error",
                    f"Syntax error: {e.msg}",
                    "Fix the syntax error to make the code executable"
                ))
                return [issue.to_dict() for issue in self.issues]
            
            # Analyze code style
            self._analyze_style(content.split('\n'), file_path)
            
            # Check imports
            self._analyze_imports(tree, file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            self.issues.append(CodeIssue(
                file_path, 1, "critical", "analysis_error",
                f"Could not analyze file: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _analyze_ast(self, tree: ast.AST, file_path: str, lines: List[str]):
        """Analyze the AST for code quality issues"""
        
        class QualityVisitor(ast.NodeVisitor):
            def __init__(self, analyzer):
                self.analyzer = analyzer
                self.file_path = file_path
                self.lines = lines
            
            def visit_FunctionDef(self, node):
                # Check function naming
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    self.analyzer.issues.append(CodeIssue(
                        self.file_path, node.lineno, "important", "naming_convention",
                        f"Function '{node.name}' should use snake_case naming",
                        f"Rename to follow snake_case convention"
                    ))
                
                # Check for missing docstring
                if not ast.get_docstring(node):
                    self.analyzer.issues.append(CodeIssue(
                        self.file_path, node.lineno, "minor", "missing_docstring",
                        f"Function '{node.name}' is missing a docstring",
                        "Add a docstring explaining the function's purpose and parameters"
                    ))
                
                # Check function length
                function_length = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if function_length > 50:
                    self.analyzer.issues.append(CodeIssue(
                        self.file_path, node.lineno, "important", "function_length",
                        f"Function '{node.name}' is {function_length} lines long (>50)",
                        "Consider breaking this function into smaller, more focused functions"
                    ))
                
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                # Check class naming
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    self.analyzer.issues.append(CodeIssue(
                        self.file_path, node.lineno, "important", "naming_convention",
                        f"Class '{node.name}' should use PascalCase naming",
                        f"Rename to follow PascalCase convention"
                    ))
                
                # Check for missing docstring
                if not ast.get_docstring(node):
                    self.analyzer.issues.append(CodeIssue(
                        self.file_path, node.lineno, "minor", "missing_docstring",
                        f"Class '{node.name}' is missing a docstring",
                        "Add a docstring explaining the class's purpose"
                    ))
                
                self.generic_visit(node)
            
            def visit_Name(self, node):
                # Check variable naming in assignments
                if isinstance(node.ctx, ast.Store):
                    if re.match(r'^[A-Z][A-Z0-9_]*$', node.id) and len(node.id) > 1:
                        # This looks like a constant, which is fine
                        pass
                    elif not re.match(r'^[a-z_][a-z0-9_]*$', node.id):
                        self.analyzer.issues.append(CodeIssue(
                            self.file_path, node.lineno, "minor", "naming_convention",
                            f"Variable '{node.id}' should use snake_case naming",
                            "Use snake_case for variable names"
                        ))
                
                self.generic_visit(node)
        
        visitor = QualityVisitor(self)
        visitor.visit(tree)
    
    def _analyze_style(self, lines: List[str], file_path: str):
        """Analyze code style issues"""
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 88:  # PEP 8 recommends 79, but 88 is more practical
                self.issues.append(CodeIssue(
                    file_path, i, "minor", "line_length",
                    f"Line {i} is {len(line)} characters long (>88)",
                    "Break long lines for better readability"
                ))
            
            # Check for tabs vs spaces
            if '\t' in line and line.strip():
                self.issues.append(CodeIssue(
                    file_path, i, "important", "indentation",
                    f"Line {i} uses tabs instead of spaces",
                    "Use 4 spaces for indentation instead of tabs"
                ))
            
            # Check for trailing whitespace
            if line.rstrip() != line and line.strip():
                self.issues.append(CodeIssue(
                    file_path, i, "minor", "trailing_whitespace",
                    f"Line {i} has trailing whitespace",
                    "Remove trailing whitespace"
                ))
            
            # Check for multiple statements on one line
            if ';' in line and not line.strip().startswith('#'):
                self.issues.append(CodeIssue(
                    file_path, i, "minor", "multiple_statements",
                    f"Line {i} has multiple statements separated by semicolon",
                    "Put each statement on its own line"
                ))
    
    def _analyze_imports(self, tree: ast.AST, file_path: str):
        """Analyze import statements"""
        
        imports_found = []
        
        class ImportVisitor(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    imports_found.append((node.lineno, alias.name))
            
            def visit_ImportFrom(self, node):
                module = node.module or ""
                for alias in node.names:
                    imports_found.append((node.lineno, f"{module}.{alias.name}"))
        
        visitor = ImportVisitor()
        visitor.visit(tree)
        
        # Check for unused imports (simplified check)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        for line_no, import_name in imports_found:
            # Simple heuristic: if import name doesn't appear elsewhere in the code
            base_name = import_name.split('.')[-1]
            if content.count(base_name) == 1:  # Only appears in the import statement
                self.issues.append(CodeIssue(
                    file_path, line_no, "minor", "unused_import",
                    f"Import '{import_name}' appears to be unused",
                    "Remove unused imports to keep code clean"
                ))


class BatchScriptAnalyzer:
    """Analyzes batch script files for quality issues"""
    
    def __init__(self):
        self.issues = []
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a batch script file for quality issues"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self._analyze_structure(lines, file_path)
            self._analyze_best_practices(lines, file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            self.issues.append(CodeIssue(
                file_path, 1, "critical", "analysis_error",
                f"Could not analyze file: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _analyze_structure(self, lines: List[str], file_path: str):
        """Analyze batch script structure"""
        
        has_echo_off = False
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for @echo off at the beginning
            if i <= 3 and line.lower() in ['@echo off', 'echo off']:
                has_echo_off = True
            
            # Check for proper variable assignment
            if '=' in line and not line.startswith('REM') and not line.startswith('::'):
                if re.search(r'set\s+\w+=\w+', line, re.IGNORECASE):
                    # Variable without quotes
                    var_match = re.search(r'set\s+(\w+)=([^"]\S*)', line, re.IGNORECASE)
                    if var_match and ' ' in var_match.group(2):
                        self.issues.append(CodeIssue(
                            file_path, i, "important", "unquoted_variable",
                            f"Variable assignment with spaces should be quoted: {line.strip()}",
                            'Use quotes: set "VAR=value with spaces"'
                        ))
            
            # Check for dangerous commands
            dangerous_patterns = [
                r'del\s+\*\.',  # del *.*
                r'rmdir\s+.*\s+/s',  # rmdir /s without /q
                r'format\s+\w+:',  # format drive
            ]
            
            for pattern in dangerous_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.issues.append(CodeIssue(
                        file_path, i, "critical", "dangerous_command",
                        f"Potentially dangerous command: {line.strip()}",
                        "Add safety checks or confirmation prompts"
                    ))
        
        if not has_echo_off:
            self.issues.append(CodeIssue(
                file_path, 1, "minor", "missing_echo_off",
                "Script doesn't have '@echo off' at the beginning",
                "Add '@echo off' to suppress command echoing"
            ))
    
    def _analyze_best_practices(self, lines: List[str], file_path: str):
        """Analyze batch script best practices"""
        
        has_exit_code = False
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for exit code
            if re.search(r'exit\s+/b\s+\d+', line, re.IGNORECASE):
                has_exit_code = True
            
            # Check for proper file existence checks
            if re.search(r'if\s+exist\s+\w+', line, re.IGNORECASE):
                if '"' not in line:
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "unquoted_filename",
                        f"File path in 'if exist' should be quoted: {line.strip()}",
                        'Use quotes around file paths: if exist "filename"'
                    ))
            
            # Check for proper error handling
            if re.search(r'copy\s+|move\s+|del\s+', line, re.IGNORECASE):
                next_line = lines[i] if i < len(lines) else ""
                if not re.search(r'if\s+errorlevel\s+|if\s+%errorlevel%', next_line, re.IGNORECASE):
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "missing_error_check",
                        f"Command should have error checking: {line.strip()}",
                        "Add error level checking after file operations"
                    ))
        
        if not has_exit_code:
            self.issues.append(CodeIssue(
                file_path, len(lines), "minor", "missing_exit_code",
                "Script doesn't have an explicit exit code",
                "Add 'exit /b 0' for success or appropriate error code"
            ))


class CSSAnalyzer:
    """Analyzes CSS files for quality and consistency issues"""
    
    def __init__(self):
        self.issues = []
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a CSS file for quality issues"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            self._analyze_formatting(lines, file_path)
            self._analyze_structure(content, file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            self.issues.append(CodeIssue(
                file_path, 1, "critical", "analysis_error",
                f"Could not analyze file: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _analyze_formatting(self, lines: List[str], file_path: str):
        """Analyze CSS formatting"""
        
        for i, line in enumerate(lines, 1):
            # Check for proper indentation
            if line.strip() and line.startswith(' '):
                indent = len(line) - len(line.lstrip())
                if indent % 2 != 0:
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "inconsistent_indentation",
                        f"Inconsistent indentation on line {i}",
                        "Use consistent 2-space indentation"
                    ))
            
            # Check for missing spaces around braces
            if '{' in line and not re.search(r'\s+{', line):
                self.issues.append(CodeIssue(
                    file_path, i, "minor", "formatting_brace",
                    f"Missing space before opening brace on line {i}",
                    "Add space before opening brace: 'selector {''"
                ))
            
            # Check for semicolon usage
            if ':' in line and line.strip().endswith('}'):
                if not line.strip().endswith(';}'):
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "missing_semicolon",
                        f"Missing semicolon before closing brace on line {i}",
                        "Add semicolon after property value"
                    ))
    
    def _analyze_structure(self, content: str, file_path: str):
        """Analyze CSS structure and organization"""
        
        # Check for vendor prefixes organization
        vendor_prefixes = ['-webkit-', '-moz-', '-ms-', '-o-']
        
        for prefix in vendor_prefixes:
            if prefix in content:
                # Count occurrences
                count = content.count(prefix)
                if count > 0:
                    self.issues.append(CodeIssue(
                        file_path, 1, "minor", "vendor_prefixes",
                        f"Found {count} vendor prefix properties ({prefix})",
                        "Consider using autoprefixer for better vendor prefix management"
                    ))
        
        # Check for duplicate selectors (simplified)
        selectors = re.findall(r'^([^{]+){', content, re.MULTILINE)
        selector_counts = {}
        
        for selector in selectors:
            selector = selector.strip()
            if selector in selector_counts:
                selector_counts[selector] += 1
            else:
                selector_counts[selector] = 1
        
        for selector, count in selector_counts.items():
            if count > 1:
                self.issues.append(CodeIssue(
                    file_path, 1, "important", "duplicate_selector",
                    f"Selector '{selector}' appears {count} times",
                    "Combine duplicate selectors or use more specific selectors"
                ))


class MarkdownAnalyzer:
    """Analyzes Markdown files for structure and formatting issues"""
    
    def __init__(self):
        self.issues = []
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a Markdown file for quality issues"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self._analyze_structure(lines, file_path)
            self._analyze_formatting(lines, file_path)
            self._analyze_links(lines, file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            self.issues.append(CodeIssue(
                file_path, 1, "critical", "analysis_error",
                f"Could not analyze file: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _analyze_structure(self, lines: List[str], file_path: str):
        """Analyze Markdown heading structure"""
        
        heading_levels = []
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for heading
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                heading_levels.append((i, level))
                
                # Check if we skip heading levels
                if len(heading_levels) > 1:
                    prev_level = heading_levels[-2][1]
                    if level > prev_level + 1:
                        self.issues.append(CodeIssue(
                            file_path, i, "minor", "structure_heading_skip",
                            f"Heading level {level} follows level {prev_level} (skipped level)",
                            "Use consecutive heading levels for better structure"
                        ))
        
        # Check if document starts with H1
        if heading_levels and heading_levels[0][1] != 1:
            first_heading_line, first_level = heading_levels[0]
            self.issues.append(CodeIssue(
                file_path, first_heading_line, "minor", "structure_no_h1",
                f"Document starts with H{first_level} instead of H1",
                "Start document with a single H1 heading"
            ))
    
    def _analyze_formatting(self, lines: List[str], file_path: str):
        """Analyze Markdown formatting"""
        
        in_code_block = False
        
        for i, line in enumerate(lines, 1):
            original_line = line
            line = line.rstrip()
            
            # Track code blocks
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                continue
            
            # Check for trailing spaces (except for line breaks)
            if original_line != line + '\n' and not line.endswith('  '):
                if original_line.rstrip() != original_line:
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "trailing_whitespace",
                        f"Line {i} has trailing whitespace",
                        "Remove trailing whitespace"
                    ))
            
            # Check list formatting
            if re.match(r'^[\s]*[-*+]\s', line):
                # Check for consistent list markers
                marker = re.search(r'([-*+])', line).group(1)
                # This is a simplified check - in reality, you'd track consistency across the document
                
                # Check for proper spacing
                if not re.match(r'^[\s]*[-*+]\s+\S', line):
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "list_formatting",
                        f"List item on line {i} has improper spacing",
                        "Use single space after list marker"
                    ))
            
            # Check for proper emphasis formatting
            if '*' in line or '_' in line:
                # Check for proper emphasis spacing
                if re.search(r'\*\S.*\S\*|\S\*.*\*\S', line):
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "emphasis_formatting",
                        f"Emphasis formatting on line {i} may have spacing issues",
                        "Ensure proper spacing around emphasis markers"
                    ))
    
    def _analyze_links(self, lines: List[str], file_path: str):
        """Analyze Markdown links"""
        
        for i, line in enumerate(lines, 1):
            # Find Markdown links
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
            
            for link_text, link_url in links:
                # Check for relative file links
                if link_url.endswith('.md') and not link_url.startswith('http'):
                    # Check if the referenced file exists
                    base_dir = Path(file_path).parent
                    target_file = base_dir / link_url
                    
                    if not target_file.exists():
                        self.issues.append(CodeIssue(
                            file_path, i, "important", "broken_link",
                            f"Link to '{link_url}' appears to be broken",
                            "Check that the referenced file exists and path is correct"
                        ))
                
                # Check for empty link text
                if not link_text.strip():
                    self.issues.append(CodeIssue(
                        file_path, i, "minor", "empty_link_text",
                        f"Link has empty text: '{link_url}'",
                        "Provide descriptive link text"
                    ))


class CodeQualityAgent:
    """Main code quality agent that coordinates all analyzers"""
    
    def __init__(self):
        self.analyzers = {
            '.py': PythonAnalyzer(),
            '.bat': BatchScriptAnalyzer(),
            '.css': CSSAnalyzer(),
            '.md': MarkdownAnalyzer(),
        }
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a file based on its extension"""
        
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension not in self.analyzers:
            return [{
                'file_path': file_path,
                'line_number': 1,
                'severity': 'minor',
                'type': 'unsupported_file_type',
                'message': f"File type '{extension}' is not supported for analysis",
                'suggestion': "Only .py, .bat, .css, and .md files are analyzed"
            }]
        
        analyzer = self.analyzers[extension]
        return analyzer.analyze_file(file_path)
    
    def analyze_directory(self, directory_path: str, 
                         file_patterns: List[str] = None) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze all supported files in a directory"""
        
        if file_patterns is None:
            file_patterns = ['*.py', '*.bat', '*.css', '*.md']
        
        results = {}
        directory = Path(directory_path)
        
        for pattern in file_patterns:
            for file_path in directory.rglob(pattern):
                if file_path.is_file():
                    relative_path = str(file_path.relative_to(directory))
                    results[relative_path] = self.analyze_file(str(file_path))
        
        return results
    
    def generate_report(self, analysis_results: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate a formatted report from analysis results"""
        
        report_lines = ["# Code Quality Analysis Report\n"]
        
        total_files = len(analysis_results)
        total_issues = sum(len(issues) for issues in analysis_results.values())
        
        report_lines.append(f"**Summary:** Analyzed {total_files} files, found {total_issues} issues\n")
        
        # Group issues by severity
        severity_counts = {'critical': 0, 'important': 0, 'minor': 0}
        
        for issues in analysis_results.values():
            for issue in issues:
                severity = issue.get('severity', 'minor')
                if severity in severity_counts:
                    severity_counts[severity] += 1
        
        report_lines.append("## Issue Summary")
        report_lines.append(f"- **Critical Issues:** {severity_counts['critical']}")
        report_lines.append(f"- **Important Issues:** {severity_counts['important']}")
        report_lines.append(f"- **Minor Issues:** {severity_counts['minor']}\n")
        
        # Detail each file
        for file_path, issues in analysis_results.items():
            if not issues:
                continue
                
            report_lines.append(f"## File: {file_path}")
            
            # Group issues by severity
            critical_issues = [i for i in issues if i.get('severity') == 'critical']
            important_issues = [i for i in issues if i.get('severity') == 'important']
            minor_issues = [i for i in issues if i.get('severity') == 'minor']
            
            for severity, issue_list in [('Critical', critical_issues), 
                                       ('Important', important_issues), 
                                       ('Minor', minor_issues)]:
                if issue_list:
                    report_lines.append(f"\n### {severity} Issues")
                    for issue in issue_list:
                        line_num = issue.get('line_number', 'N/A')
                        message = issue.get('message', 'No message')
                        suggestion = issue.get('suggestion', '')
                        
                        report_lines.append(f"- **Line {line_num}:** {message}")
                        if suggestion:
                            report_lines.append(f"  - *Suggestion:* {suggestion}")
            
            report_lines.append("")  # Empty line between files
        
        return "\n".join(report_lines)


def main():
    """Command-line interface for the code quality agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze code quality")
    parser.add_argument("path", help="File or directory to analyze")
    parser.add_argument("--format", choices=["json", "report"], default="report",
                       help="Output format")
    
    args = parser.parse_args()
    
    agent = CodeQualityAgent()
    
    if Path(args.path).is_file():
        # Analyze single file
        results = {args.path: agent.analyze_file(args.path)}
    else:
        # Analyze directory
        results = agent.analyze_directory(args.path)
    
    if args.format == "json":
        import json
        print(json.dumps(results, indent=2))
    else:
        report = agent.generate_report(results)
        print(report)


if __name__ == "__main__":
    main()