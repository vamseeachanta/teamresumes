#!/usr/bin/env python3
"""
Documentation Agent Implementation
Maintains documentation consistency, updates cross-references, and generates documentation
"""

import ast
import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentationIssue:
    """Represents a documentation issue"""
    
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


class LinkValidator:
    """Validates links in markdown documents"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.issues = []
    
    def validate_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Validate all links in a markdown file"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self._validate_markdown_links(lines, file_path)
            self._validate_anchor_links(lines, file_path)
            
        except Exception as e:
            logger.error(f"Error validating links in {file_path}: {e}")
            self.issues.append(DocumentationIssue(
                file_path, 1, "critical", "validation_error",
                f"Could not validate links: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _validate_markdown_links(self, lines: List[str], file_path: str):
        """Validate markdown links [text](url)"""
        
        for i, line in enumerate(lines, 1):
            # Find all markdown links
            links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', line)
            
            for link_text, link_url in links:
                # Skip external links (basic validation)
                if self._is_external_link(link_url):
                    self._validate_external_link(link_url, file_path, i)
                    continue
                
                # Validate internal links
                self._validate_internal_link(link_url, file_path, i)
                
                # Check for empty link text
                if not link_text.strip():
                    self.issues.append(DocumentationIssue(
                        file_path, i, "minor", "empty_link_text",
                        f"Link has empty text: '{link_url}'",
                        "Provide descriptive link text"
                    ))
    
    def _validate_anchor_links(self, lines: List[str], file_path: str):
        """Validate anchor links within the document"""
        
        # Find all headings to build valid anchor list
        valid_anchors = set()
        for line in lines:
            if line.strip().startswith('#'):
                heading = line.strip().lstrip('#').strip()
                # Convert to anchor format (simplified)
                anchor = heading.lower().replace(' ', '-').replace('.', '').replace(',', '')
                valid_anchors.add(f"#{anchor}")
        
        # Check anchor links
        for i, line in enumerate(lines, 1):
            anchor_links = re.findall(r'\[([^\]]*)\]\((#[^)]+)\)', line)
            
            for link_text, anchor in anchor_links:
                if anchor not in valid_anchors:
                    self.issues.append(DocumentationIssue(
                        file_path, i, "important", "broken_anchor",
                        f"Anchor link '{anchor}' not found in document",
                        "Check that the referenced section exists"
                    ))
    
    def _is_external_link(self, url: str) -> bool:
        """Check if a URL is external"""
        return url.startswith(('http://', 'https://', 'mailto:', 'ftp://'))
    
    def _validate_external_link(self, url: str, file_path: str, line_number: int):
        """Validate external links (basic checks)"""
        
        parsed = urlparse(url)
        
        # Check for valid protocol
        if parsed.scheme not in ['http', 'https', 'mailto']:
            self.issues.append(DocumentationIssue(
                file_path, line_number, "minor", "unusual_protocol",
                f"External link uses unusual protocol: {url}",
                "Consider using https:// for web links"
            ))
        
        # Check for suspicious patterns
        if 'localhost' in url or '127.0.0.1' in url:
            self.issues.append(DocumentationIssue(
                file_path, line_number, "important", "localhost_link",
                f"Link points to localhost: {url}",
                "Replace with actual public URL or remove"
            ))
    
    def _validate_internal_link(self, url: str, file_path: str, line_number: int):
        """Validate internal file links"""
        
        # Handle anchor-only links
        if url.startswith('#'):
            return  # Handled by _validate_anchor_links
        
        # Resolve relative path
        current_dir = Path(file_path).parent
        
        # Handle anchor in file link
        if '#' in url:
            url_parts = url.split('#', 1)
            target_file = url_parts[0]
            anchor = f"#{url_parts[1]}"
        else:
            target_file = url
            anchor = None
        
        # Resolve target file path
        if target_file.startswith('/'):
            # Absolute path from project root
            target_path = self.project_root / target_file.lstrip('/')
        else:
            # Relative path
            target_path = current_dir / target_file
        
        try:
            target_path = target_path.resolve()
            
            # Check if target is within project
            try:
                target_path.relative_to(self.project_root)
            except ValueError:
                self.issues.append(DocumentationIssue(
                    file_path, line_number, "important", "external_file_link",
                    f"Link points outside project: {url}",
                    "Use relative paths within the project"
                ))
                return
            
            # Check if file exists
            if not target_path.exists():
                self.issues.append(DocumentationIssue(
                    file_path, line_number, "important", "broken_link",
                    f"Link target does not exist: {url}",
                    "Check that the referenced file exists and path is correct"
                ))
                return
            
            # If there's an anchor, validate it in the target file
            if anchor and target_path.suffix.lower() == '.md':
                self._validate_anchor_in_file(anchor, target_path, file_path, line_number)
                
        except Exception as e:
            self.issues.append(DocumentationIssue(
                file_path, line_number, "important", "link_resolution_error",
                f"Could not resolve link: {url} - {e}",
                "Check link path and syntax"
            ))
    
    def _validate_anchor_in_file(self, anchor: str, target_file: Path, 
                                source_file: str, line_number: int):
        """Validate anchor exists in target file"""
        
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                target_content = f.read()
            
            # Find headings in target file
            headings = re.findall(r'^#+\s+(.+)$', target_content, re.MULTILINE)
            valid_anchors = set()
            
            for heading in headings:
                # Convert to anchor format
                anchor_text = heading.lower().replace(' ', '-').replace('.', '').replace(',', '')
                valid_anchors.add(f"#{anchor_text}")
            
            if anchor not in valid_anchors:
                self.issues.append(DocumentationIssue(
                    source_file, line_number, "important", "broken_anchor_reference",
                    f"Anchor '{anchor}' not found in {target_file.name}",
                    f"Check available sections in {target_file.name}"
                ))
                
        except Exception as e:
            logger.warning(f"Could not validate anchor in {target_file}: {e}")


class CrossReferenceValidator:
    """Validates Agent OS cross-references (@ syntax)"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.issues = []
    
    def validate_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Validate all cross-references in a file"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self._validate_cross_references(lines, file_path)
            
        except Exception as e:
            logger.error(f"Error validating cross-references in {file_path}: {e}")
            self.issues.append(DocumentationIssue(
                file_path, 1, "critical", "validation_error",
                f"Could not validate cross-references: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _validate_cross_references(self, lines: List[str], file_path: str):
        """Validate @ cross-references"""
        
        for i, line in enumerate(lines, 1):
            # Find all @ references
            references = re.findall(r'@([^\s\)]+)', line)
            
            for ref in references:
                self._validate_single_reference(ref, file_path, i)
    
    def _validate_single_reference(self, ref: str, file_path: str, line_number: int):
        """Validate a single cross-reference"""
        
        # Handle different reference types
        if ref.startswith('.agent-os/'):
            self._validate_agent_os_reference(ref, file_path, line_number)
        elif ref.startswith('~/.agent-os/'):
            self._validate_global_agent_os_reference(ref, file_path, line_number)
        elif ref.startswith('./') or '/' in ref:
            self._validate_relative_reference(ref, file_path, line_number)
        else:
            self.issues.append(DocumentationIssue(
                file_path, line_number, "minor", "unknown_reference_type",
                f"Unknown reference type: @{ref}",
                "Use standard reference formats (@.agent-os/, @~/.agent-os/, or relative paths)"
            ))
    
    def _validate_agent_os_reference(self, ref: str, file_path: str, line_number: int):
        """Validate .agent-os/ references"""
        
        target_path = self.project_root / ref
        
        if not target_path.exists():
            self.issues.append(DocumentationIssue(
                file_path, line_number, "important", "broken_cross_reference",
                f"Cross-reference target does not exist: @{ref}",
                "Check that the referenced file exists in the Agent OS structure"
            ))
            return
        
        # Validate specific Agent OS patterns
        if ref.startswith('.agent-os/product/'):
            self._validate_product_reference(ref, file_path, line_number)
        elif ref.startswith('.agent-os/specs/'):
            self._validate_spec_reference(ref, file_path, line_number)
    
    def _validate_global_agent_os_reference(self, ref: str, file_path: str, line_number: int):
        """Validate ~/.agent-os/ references (global Agent OS)"""
        
        # These are references to global Agent OS files
        # For testing purposes, we'll assume they exist
        # In a real implementation, you might check user's home directory
        
        expected_global_files = [
            '~/.agent-os/standards/tech-stack.md',
            '~/.agent-os/standards/code-style.md',
            '~/.agent-os/standards/best-practices.md',
            '~/.agent-os/instructions/plan-product.md',
            '~/.agent-os/instructions/create-spec.md',
            '~/.agent-os/instructions/execute-tasks.md',
            '~/.agent-os/instructions/analyze-product.md'
        ]
        
        if ref not in [r.replace('~/.agent-os/', '') for r in expected_global_files]:
            self.issues.append(DocumentationIssue(
                file_path, line_number, "minor", "unknown_global_reference",
                f"Reference to unknown global Agent OS file: @{ref}",
                "Check if this is a valid global Agent OS file"
            ))
    
    def _validate_relative_reference(self, ref: str, file_path: str, line_number: int):
        """Validate relative path references"""
        
        current_dir = Path(file_path).parent
        target_path = current_dir / ref
        
        try:
            target_path = target_path.resolve()
            
            if not target_path.exists():
                self.issues.append(DocumentationIssue(
                    file_path, line_number, "important", "broken_relative_reference",
                    f"Relative reference target does not exist: @{ref}",
                    "Check that the referenced file exists at the specified path"
                ))
        except Exception as e:
            self.issues.append(DocumentationIssue(
                file_path, line_number, "important", "reference_resolution_error",
                f"Could not resolve relative reference: @{ref} - {e}",
                "Check reference path syntax"
            ))
    
    def _validate_product_reference(self, ref: str, file_path: str, line_number: int):
        """Validate product-specific references"""
        
        valid_product_files = [
            '.agent-os/product/mission.md',
            '.agent-os/product/tech-stack.md',
            '.agent-os/product/roadmap.md',
            '.agent-os/product/decisions.md'
        ]
        
        if ref not in valid_product_files:
            self.issues.append(DocumentationIssue(
                file_path, line_number, "minor", "unusual_product_reference",
                f"Reference to non-standard product file: @{ref}",
                "Standard product files are mission.md, tech-stack.md, roadmap.md, decisions.md"
            ))
    
    def _validate_spec_reference(self, ref: str, file_path: str, line_number: int):
        """Validate spec-specific references"""
        
        # Check spec reference format
        spec_pattern = r'\.agent-os/specs/\d{4}-\d{2}-\d{2}-[^/]+/.+\.md$'
        
        if not re.match(spec_pattern, ref):
            self.issues.append(DocumentationIssue(
                file_path, line_number, "minor", "non_standard_spec_reference",
                f"Spec reference doesn't follow standard format: @{ref}",
                "Use format: .agent-os/specs/YYYY-MM-DD-spec-name/file.md"
            ))


class ReadmeAnalyzer:
    """Analyzes and maintains README.md files"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.issues = []
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze README.md structure and content"""
        self.issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            self._analyze_structure(lines, file_path)
            self._analyze_content_freshness(content, file_path)
            self._check_required_sections(lines, file_path)
            
        except Exception as e:
            logger.error(f"Error analyzing README {file_path}: {e}")
            self.issues.append(DocumentationIssue(
                file_path, 1, "critical", "analysis_error",
                f"Could not analyze README: {e}",
                "Check file encoding and permissions"
            ))
        
        return [issue.to_dict() for issue in self.issues]
    
    def _analyze_structure(self, lines: List[str], file_path: str):
        """Analyze README structure"""
        
        # Check for title (H1)
        has_title = False
        first_heading_line = None
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                if first_heading_line is None:
                    first_heading_line = i
                    if line.strip().startswith('# '):
                        has_title = True
                break
        
        if not has_title:
            if first_heading_line:
                self.issues.append(DocumentationIssue(
                    file_path, first_heading_line, "important", "missing_title",
                    "README should start with H1 title",
                    "Add a clear project title using # Title"
                ))
            else:
                self.issues.append(DocumentationIssue(
                    file_path, 1, "important", "missing_title",
                    "README has no title or headings",
                    "Add a clear project title and structure"
                ))
    
    def _analyze_content_freshness(self, content: str, file_path: str):
        """Analyze if README content seems fresh and relevant"""
        
        # Check for common outdated indicators
        outdated_indicators = [
            'TODO',
            'coming soon',
            'under construction',
            'work in progress',
            'TBD',
            'placeholder'
        ]
        
        content_lower = content.lower()
        
        for indicator in outdated_indicators:
            if indicator in content_lower:
                self.issues.append(DocumentationIssue(
                    file_path, 1, "minor", "potentially_outdated",
                    f"README contains potentially outdated text: '{indicator}'",
                    "Review and update outdated placeholder content"
                ))
        
        # Check length - very short READMEs might need more content
        if len(content.strip()) < 200:
            self.issues.append(DocumentationIssue(
                file_path, 1, "minor", "brief_content",
                "README is quite brief (less than 200 characters)",
                "Consider adding more detailed project description and usage instructions"
            ))
    
    def _check_required_sections(self, lines: List[str], file_path: str):
        """Check for common README sections"""
        
        content = '\n'.join(lines).lower()
        
        # Common sections that should be present
        recommended_sections = {
            'installation': ['installation', 'install', 'setup', 'getting started'],
            'usage': ['usage', 'how to use', 'examples', 'quick start'],
            'features': ['features', 'what it does', 'capabilities'],
        }
        
        for section_name, keywords in recommended_sections.items():
            found = any(keyword in content for keyword in keywords)
            
            if not found:
                self.issues.append(DocumentationIssue(
                    file_path, 1, "minor", "missing_section",
                    f"README appears to be missing {section_name} section",
                    f"Consider adding a section about {section_name}"
                ))
        
        # Check if there are any code examples
        has_code_blocks = '```' in content or '    ' in content  # Code blocks or indented code
        
        if not has_code_blocks:
            self.issues.append(DocumentationIssue(
                file_path, 1, "minor", "missing_examples",
                "README doesn't contain code examples",
                "Consider adding usage examples with code blocks"
            ))


class ApiDocumentationGenerator:
    """Generates API documentation from Python code"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
    
    def generate_from_file(self, file_path: str) -> str:
        """Generate API documentation from a Python file"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=file_path)
            
            docs = []
            docs.append(f"# API Documentation: {Path(file_path).name}\n")
            
            # Extract functions and classes
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if not node.name.startswith('_'):  # Public functions only
                        func_doc = self._generate_function_docs(node)
                        if func_doc:
                            docs.append(func_doc)
                
                elif isinstance(node, ast.ClassDef):
                    class_doc = self._generate_class_docs(node)
                    if class_doc:
                        docs.append(class_doc)
            
            return '\n'.join(docs)
            
        except Exception as e:
            logger.error(f"Error generating API docs for {file_path}: {e}")
            return f"# Error generating documentation for {Path(file_path).name}\n\nError: {e}"
    
    def _generate_function_docs(self, node: ast.FunctionDef) -> str:
        """Generate documentation for a function"""
        
        docs = [f"\n## Function: `{node.name}`\n"]
        
        # Get docstring
        docstring = ast.get_docstring(node)
        if docstring:
            docs.append(f"{docstring}\n")
        else:
            docs.append("*No documentation available*\n")
        
        # Get function signature
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        
        signature = f"{node.name}({', '.join(args)})"
        docs.append(f"**Signature:** `{signature}`\n")
        
        return '\n'.join(docs)
    
    def _generate_class_docs(self, node: ast.ClassDef) -> str:
        """Generate documentation for a class"""
        
        docs = [f"\n## Class: `{node.name}`\n"]
        
        # Get docstring
        docstring = ast.get_docstring(node)
        if docstring:
            docs.append(f"{docstring}\n")
        else:
            docs.append("*No documentation available*\n")
        
        # Get public methods
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and not item.name.startswith('_'):
                methods.append(item.name)
        
        if methods:
            docs.append("**Public Methods:**")
            for method in methods:
                docs.append(f"- `{method}()`")
            docs.append("")
        
        return '\n'.join(docs)


class ProjectStructureGenerator:
    """Generates project structure documentation"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
    
    def generate_structure_docs(self) -> str:
        """Generate project structure documentation"""
        
        docs = ["# Project Structure\n"]
        
        # Generate directory tree
        tree = self._generate_tree_structure()
        docs.append("## Directory Structure\n")
        docs.append("```")
        docs.append(tree)
        docs.append("```\n")
        
        # Add descriptions for key directories
        key_dirs = self._analyze_key_directories()
        if key_dirs:
            docs.append("## Directory Descriptions\n")
            for dir_path, description in key_dirs.items():
                docs.append(f"- **{dir_path}**: {description}")
            docs.append("")
        
        return '\n'.join(docs)
    
    def _generate_tree_structure(self, max_depth: int = 3) -> str:
        """Generate ASCII tree structure"""
        
        def _build_tree(path: Path, prefix: str = "", depth: int = 0) -> List[str]:
            if depth > max_depth:
                return []
            
            items = []
            try:
                children = list(path.iterdir())
                children.sort(key=lambda x: (x.is_file(), x.name.lower()))
                
                for i, child in enumerate(children):
                    if child.name.startswith('.') and child.name not in ['.agent-os', '.claude']:
                        continue
                    
                    is_last = i == len(children) - 1
                    current_prefix = "└── " if is_last else "├── "
                    items.append(f"{prefix}{current_prefix}{child.name}")
                    
                    if child.is_dir() and depth < max_depth:
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        items.extend(_build_tree(child, next_prefix, depth + 1))
                        
            except PermissionError:
                items.append(f"{prefix}├── [Permission Denied]")
            
            return items
        
        tree_lines = [self.project_root.name]
        tree_lines.extend(_build_tree(self.project_root))
        
        return '\n'.join(tree_lines)
    
    def _analyze_key_directories(self) -> Dict[str, str]:
        """Analyze and describe key directories"""
        
        descriptions = {}
        
        common_dirs = {
            'src': 'Source code directory',
            'lib': 'Library files',
            'docs': 'Documentation files',
            'tests': 'Test files',
            'examples': 'Example code and usage',
            'scripts': 'Utility scripts',
            'tools': 'Development tools',
            'config': 'Configuration files',
            'data': 'Data files',
            'assets': 'Static assets',
            '.agent-os': 'Agent OS configuration and specifications',
            '.claude': 'Claude Code configuration',
            'cv': 'Resume and CV files',
            'dev_tools': 'Development tools and utilities'
        }
        
        for dir_name, description in common_dirs.items():
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                descriptions[dir_name] = description
        
        return descriptions


class DocumentationAgent:
    """Main documentation agent that coordinates all analyzers"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.link_validator = LinkValidator(str(self.project_root))
        self.cross_ref_validator = CrossReferenceValidator(str(self.project_root))
        self.readme_analyzer = ReadmeAnalyzer(str(self.project_root))
        self.api_generator = ApiDocumentationGenerator(str(self.project_root))
        self.structure_generator = ProjectStructureGenerator(str(self.project_root))
    
    def analyze_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Analyze a documentation file"""
        
        path = Path(file_path)
        all_issues = []
        
        # Only analyze markdown files
        if path.suffix.lower() != '.md':
            return [{
                'file_path': file_path,
                'line_number': 1,
                'severity': 'minor',
                'type': 'unsupported_file_type',
                'message': f"File type '{path.suffix}' is not supported for documentation analysis",
                'suggestion': "Only .md files are analyzed by the documentation agent"
            }]
        
        # Validate links
        link_issues = self.link_validator.validate_file(file_path)
        all_issues.extend(link_issues)
        
        # Validate cross-references
        cross_ref_issues = self.cross_ref_validator.validate_file(file_path)
        all_issues.extend(cross_ref_issues)
        
        # Special handling for README files
        if path.name.lower() == 'readme.md':
            readme_issues = self.readme_analyzer.analyze_file(file_path)
            all_issues.extend(readme_issues)
        
        return all_issues
    
    def analyze_project_documentation(self) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze all documentation in the project"""
        
        results = {}
        
        # Find all markdown files
        for md_file in self.project_root.rglob('*.md'):
            try:
                relative_path = str(md_file.relative_to(self.project_root))
                results[relative_path] = self.analyze_file(str(md_file))
            except Exception as e:
                logger.error(f"Error analyzing {md_file}: {e}")
                results[str(md_file)] = [{
                    'file_path': str(md_file),
                    'line_number': 1,
                    'severity': 'critical',
                    'type': 'analysis_error',
                    'message': f"Could not analyze file: {e}",
                    'suggestion': "Check file permissions and encoding"
                }]
        
        return results
    
    def generate_api_documentation(self, python_files: List[str] = None) -> str:
        """Generate API documentation for Python files"""
        
        if python_files is None:
            python_files = list(self.project_root.rglob('*.py'))
        
        all_docs = ["# Project API Documentation\n"]
        
        for py_file in python_files:
            if isinstance(py_file, str):
                py_file = Path(py_file)
            
            if py_file.name.startswith('test_') or py_file.name.endswith('_test.py'):
                continue  # Skip test files
            
            try:
                file_docs = self.api_generator.generate_from_file(str(py_file))
                all_docs.append(file_docs)
            except Exception as e:
                logger.error(f"Error generating API docs for {py_file}: {e}")
        
        return '\n'.join(all_docs)
    
    def generate_project_structure_docs(self) -> str:
        """Generate project structure documentation"""
        return self.structure_generator.generate_structure_docs()
    
    def generate_report(self, analysis_results: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate a formatted documentation analysis report"""
        
        report_lines = ["# Documentation Analysis Report\n"]
        
        total_files = len(analysis_results)
        total_issues = sum(len(issues) for issues in analysis_results.values())
        
        report_lines.append(f"**Summary:** Analyzed {total_files} documentation files, found {total_issues} issues\n")
        
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
    """Command-line interface for the documentation agent"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze documentation quality")
    parser.add_argument("path", help="File or directory to analyze")
    parser.add_argument("--format", choices=["json", "report"], default="report",
                       help="Output format")
    parser.add_argument("--generate-api", action="store_true",
                       help="Generate API documentation")
    parser.add_argument("--generate-structure", action="store_true", 
                       help="Generate project structure documentation")
    
    args = parser.parse_args()
    
    agent = DocumentationAgent()
    
    if args.generate_api:
        api_docs = agent.generate_api_documentation()
        print(api_docs)
        return
    
    if args.generate_structure:
        structure_docs = agent.generate_project_structure_docs()
        print(structure_docs)
        return
    
    if Path(args.path).is_file():
        # Analyze single file
        results = {args.path: agent.analyze_file(args.path)}
    else:
        # Analyze all documentation
        results = agent.analyze_project_documentation()
    
    if args.format == "json":
        import json
        print(json.dumps(results, indent=2))
    else:
        report = agent.generate_report(results)
        print(report)


if __name__ == "__main__":
    main()