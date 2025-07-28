#!/usr/bin/env python3
"""
Code Quality Agent Test Suite
Tests for the code quality analysis functionality
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class TestPythonAnalysis(unittest.TestCase):
    """Test Python code analysis functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_valid_python_code(self):
        """Test analysis of valid Python code"""
        valid_code = '''
def calculate_sum(a, b):
    """Calculate the sum of two numbers."""
    return a + b

class Calculator:
    """A simple calculator class."""
    
    def __init__(self):
        self.result = 0
    
    def add(self, value):
        """Add a value to the result."""
        self.result += value
        return self.result
'''
        
        file_path = self.create_test_file("valid.py", valid_code)
        
        # Import here to avoid circular imports during test discovery
        from code_quality_agent import PythonAnalyzer
        analyzer = PythonAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should have minimal or no issues
        critical_issues = [issue for issue in issues if issue['severity'] == 'critical']
        self.assertEqual(len(critical_issues), 0, "Valid code should not have critical issues")
    
    def test_python_syntax_error(self):
        """Test detection of Python syntax errors"""
        invalid_code = '''
def broken_function(
    print("This has a syntax error")
    return "missing closing parenthesis"
'''
        
        file_path = self.create_test_file("invalid.py", invalid_code)
        
        from code_quality_agent import PythonAnalyzer
        analyzer = PythonAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should detect syntax error
        critical_issues = [issue for issue in issues if issue['severity'] == 'critical']
        self.assertGreater(len(critical_issues), 0, "Should detect syntax error")
    
    def test_python_style_issues(self):
        """Test detection of Python style issues"""
        style_issues_code = '''
def badFunction(x,y):
    if x>0:
        return x+y
    else:
        return x-y

class badClass:
    def __init__(self,value):
        self.Value=value
'''
        
        file_path = self.create_test_file("style_issues.py", style_issues_code)
        
        from code_quality_agent import PythonAnalyzer
        analyzer = PythonAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should detect naming and formatting issues
        naming_issues = [issue for issue in issues if 'naming' in issue['type'].lower()]
        self.assertGreater(len(naming_issues), 0, "Should detect naming convention issues")
    
    def test_missing_docstrings(self):
        """Test detection of missing docstrings"""
        no_docstring_code = '''
def function_without_docstring(x, y):
    return x + y

class ClassWithoutDocstring:
    def method_without_docstring(self):
        pass
'''
        
        file_path = self.create_test_file("no_docstrings.py", no_docstring_code)
        
        from code_quality_agent import PythonAnalyzer
        analyzer = PythonAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should detect missing docstrings
        docstring_issues = [issue for issue in issues if 'docstring' in issue['type'].lower()]
        self.assertGreater(len(docstring_issues), 0, "Should detect missing docstrings")


class TestBatchScriptAnalysis(unittest.TestCase):
    """Test batch script analysis functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_valid_batch_script(self):
        """Test analysis of valid batch script"""
        valid_batch = '''@echo off
REM This is a valid batch script
set "VAR=value"
if exist "file.txt" (
    echo File exists
    del "file.txt"
)
exit /b 0
'''
        
        file_path = self.create_test_file("valid.bat", valid_batch)
        
        from code_quality_agent import BatchScriptAnalyzer
        analyzer = BatchScriptAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should have minimal issues
        critical_issues = [issue for issue in issues if issue['severity'] == 'critical']
        self.assertEqual(len(critical_issues), 0, "Valid batch script should not have critical issues")
    
    def test_batch_script_issues(self):
        """Test detection of batch script issues"""
        problematic_batch = '''echo off
set VAR=value with spaces
if exist file.txt echo File exists
del *.txt
'''
        
        file_path = self.create_test_file("issues.bat", problematic_batch)
        
        from code_quality_agent import BatchScriptAnalyzer
        analyzer = BatchScriptAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should detect various issues
        self.assertGreater(len(issues), 0, "Should detect batch script issues")


class TestCSSAnalysis(unittest.TestCase):
    """Test CSS analysis functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_valid_css(self):
        """Test analysis of valid CSS"""
        valid_css = '''
/* Resume stylesheet */
body {
  font-family: 'Arial', sans-serif;
  font-size: 12pt;
  line-height: 1.4;
  margin: 0;
  padding: 20px;
}

h1, h2, h3 {
  color: #333;
  font-weight: bold;
}

.section {
  margin-bottom: 20px;
  padding: 10px;
}
'''
        
        file_path = self.create_test_file("valid.css", valid_css)
        
        from code_quality_agent import CSSAnalyzer
        analyzer = CSSAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should have minimal issues
        critical_issues = [issue for issue in issues if issue['severity'] == 'critical']
        self.assertEqual(len(critical_issues), 0, "Valid CSS should not have critical issues")
    
    def test_css_formatting_issues(self):
        """Test detection of CSS formatting issues"""
        messy_css = '''
body{font-family:Arial;font-size:12pt;margin:0;padding:20px;}
h1,h2,h3{color:#333;font-weight:bold;}
.section{margin-bottom:20px;padding:10px;}
'''
        
        file_path = self.create_test_file("messy.css", messy_css)
        
        from code_quality_agent import CSSAnalyzer
        analyzer = CSSAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should detect formatting issues
        formatting_issues = [issue for issue in issues if 'formatting' in issue['type'].lower()]
        self.assertGreater(len(formatting_issues), 0, "Should detect CSS formatting issues")


class TestMarkdownAnalysis(unittest.TestCase):
    """Test Markdown analysis functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file with given content"""
        file_path = self.temp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_valid_markdown(self):
        """Test analysis of valid Markdown"""
        valid_md = '''# Resume Title

## Professional Experience

### Senior Software Engineer
**Company Name** | *2020 - Present*

- Developed and maintained web applications
- Led team of 5 developers
- Improved system performance by 30%

## Skills

- Python, JavaScript, SQL
- React, Node.js, PostgreSQL
- AWS, Docker, Kubernetes

## Education

**Bachelor of Science in Computer Science**  
University Name | 2018
'''
        
        file_path = self.create_test_file("valid.md", valid_md)
        
        from code_quality_agent import MarkdownAnalyzer
        analyzer = MarkdownAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should have minimal issues
        critical_issues = [issue for issue in issues if issue['severity'] == 'critical']
        self.assertEqual(len(critical_issues), 0, "Valid Markdown should not have critical issues")
    
    def test_markdown_structure_issues(self):
        """Test detection of Markdown structure issues"""
        problematic_md = '''##### This starts with H5 instead of H1

# Title
### This skips H2 and goes to H3

## Section
- List item
- Another item
  - Inconsistent indentation
    - More inconsistent indentation

[Broken link](nonexistent-file.md)
'''
        
        file_path = self.create_test_file("issues.md", problematic_md)
        
        from code_quality_agent import MarkdownAnalyzer
        analyzer = MarkdownAnalyzer()
        issues = analyzer.analyze_file(str(file_path))
        
        # Should detect structure issues
        structure_issues = [issue for issue in issues if 'structure' in issue['type'].lower()]
        self.assertGreater(len(structure_issues), 0, "Should detect Markdown structure issues")


class TestCodeQualityIntegration(unittest.TestCase):
    """Test integration with the agent framework"""
    
    def test_agent_configuration(self):
        """Test that the code quality agent configuration is valid"""
        from agent_config_parser import AgentConfigParser
        
        parser = AgentConfigParser()
        agents = parser.load_all_agents()  # Load agents first
        config = parser.get_agent_config("code-quality-agent")
        
        self.assertIsNotNone(config, "Code quality agent configuration should exist")
        self.assertEqual(config['name'], "code-quality-agent")
        self.assertEqual(config['specialization'], "code-review-and-formatting")
    
    def test_security_integration(self):
        """Test that the code quality agent works with security framework"""
        from security_framework import SecurityFramework, PermissionType
        from agent_config_parser import AgentConfigParser
        
        parser = AgentConfigParser()
        agents = parser.load_all_agents()  # Load agents first
        config = parser.get_agent_config("code-quality-agent")
        
        framework = SecurityFramework()
        session_id = framework.create_session("code-quality-agent", config)
        
        # Test permissions
        can_read_python = framework.check_permission(
            session_id, PermissionType.READ, "test.py", config
        )
        can_write_python = framework.check_permission(
            session_id, PermissionType.WRITE, "test.py", config
        )
        
        self.assertTrue(can_read_python, "Should be able to read Python files")
        self.assertTrue(can_write_python, "Should be able to write Python files")
        
        framework.end_session(session_id)


def run_tests():
    """Run all code quality agent tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestPythonAnalysis,
        TestBatchScriptAnalysis,
        TestCSSAnalysis,
        TestMarkdownAnalysis,
        TestCodeQualityIntegration
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)