#!/usr/bin/env python3
"""
Maintenance Agent Test Suite
Tests for dependency monitoring, security scanning, and project health monitoring
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
import json

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

class TestDependencyMonitoring(unittest.TestCase):
    """Test dependency monitoring and analysis functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file"""
        file_path = self.temp_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_python_dependencies_analysis(self):
        """Test analysis of Python dependencies"""
        requirements_content = """pandas==1.5.3
matplotlib==3.7.1
scipy==1.10.1
plotly==5.14.1
pytest==7.3.1
black==23.3.0
# Development dependencies
isort==5.12.0
flake8==6.0.0
"""
        
        file_path = self.create_test_file("requirements.txt", requirements_content)
        
        from maintenance_agent import DependencyAnalyzer
        analyzer = DependencyAnalyzer()
        deps = analyzer.analyze_python_dependencies(str(file_path))
        
        # Should identify all dependencies
        self.assertGreater(len(deps), 0, "Should find Python dependencies")
        
        # Check for key packages
        dep_names = [dep['name'] for dep in deps]
        self.assertIn('pandas', dep_names, "Should include pandas")
        self.assertIn('matplotlib', dep_names, "Should include matplotlib")
        
        # Check version parsing
        pandas_dep = next(dep for dep in deps if dep['name'] == 'pandas')
        self.assertEqual(pandas_dep['version'], '1.5.3', "Should parse version correctly")
    
    def test_outdated_dependencies_detection(self):
        """Test detection of outdated dependencies"""
        requirements_content = """pandas==1.3.0
matplotlib==3.5.0
scipy==1.8.0
"""
        
        file_path = self.create_test_file("requirements.txt", requirements_content)
        
        from maintenance_agent import DependencyAnalyzer
        analyzer = DependencyAnalyzer()
        outdated = analyzer.check_outdated_dependencies(str(file_path))
        
        # Should detect potentially outdated packages
        self.assertIsInstance(outdated, list, "Should return list of outdated packages")
        
        # Check structure of outdated info
        if outdated:
            for pkg in outdated:
                self.assertIn('name', pkg, "Should include package name")
                self.assertIn('current_version', pkg, "Should include current version")
                self.assertIn('latest_version', pkg, "Should include latest version")
    
    def test_dependency_vulnerability_check(self):
        """Test checking for known vulnerabilities in dependencies"""
        requirements_content = """requests==2.25.0
urllib3==1.26.0
jinja2==2.11.0
"""
        
        file_path = self.create_test_file("requirements.txt", requirements_content)
        
        from maintenance_agent import SecurityScanner
        scanner = SecurityScanner()
        vulnerabilities = scanner.scan_dependencies(str(file_path))
        
        # Should return vulnerability analysis
        self.assertIsInstance(vulnerabilities, dict, "Should return vulnerability report")
        self.assertIn('scanned_packages', vulnerabilities, "Should include scanned packages count")
        self.assertIn('vulnerabilities_found', vulnerabilities, "Should include vulnerabilities found")
    
    def test_package_json_analysis(self):
        """Test analysis of Node.js package.json dependencies"""
        package_json_content = """{
  "name": "teamresumes-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.0.0"
  },
  "devDependencies": {
    "vite": "^4.3.0",
    "@types/react": "^18.0.37",
    "eslint": "^8.40.0"
  }
}"""
        
        file_path = self.create_test_file("package.json", package_json_content)
        
        from maintenance_agent import DependencyAnalyzer
        analyzer = DependencyAnalyzer()
        deps = analyzer.analyze_nodejs_dependencies(str(file_path))
        
        # Should identify dependencies
        self.assertGreater(len(deps), 0, "Should find Node.js dependencies")
        
        # Check for React
        dep_names = [dep['name'] for dep in deps]
        self.assertIn('react', dep_names, "Should include React")
        self.assertIn('typescript', dep_names, "Should include TypeScript")


class TestSecurityScanning(unittest.TestCase):
    """Test security vulnerability scanning functionality"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file"""
        file_path = self.temp_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_code_security_scan(self):
        """Test security scanning of code files"""
        python_code = '''
import os
import subprocess

# Potential security issue - using shell=True
def execute_command(user_input):
    subprocess.run(f"echo {user_input}", shell=True)

# Another potential issue - direct SQL query
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return query

# Hardcoded credentials (security issue)
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "admin123"
'''
        
        file_path = self.create_test_file("vulnerable_code.py", python_code)
        
        from maintenance_agent import SecurityScanner
        scanner = SecurityScanner()
        issues = scanner.scan_code_security(str(file_path))
        
        # Should detect security issues
        self.assertIsInstance(issues, list, "Should return list of security issues")
        
        # Check issue structure
        if issues:
            for issue in issues:
                self.assertIn('type', issue, "Should include issue type")
                self.assertIn('severity', issue, "Should include severity level")
                self.assertIn('line', issue, "Should include line number")
                self.assertIn('description', issue, "Should include description")
    
    def test_secrets_detection(self):
        """Test detection of hardcoded secrets"""
        config_content = '''
# Configuration file
DATABASE_URL=postgresql://user:password123@localhost/db
API_KEY=sk-abcd1234567890
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
GITHUB_TOKEN=ghp_1234567890abcdef

# These should not trigger
LOG_LEVEL=DEBUG
MAX_CONNECTIONS=100
'''
        
        file_path = self.create_test_file(".env", config_content)
        
        from maintenance_agent import SecurityScanner
        scanner = SecurityScanner()
        secrets = scanner.detect_secrets(str(file_path))
        
        # Should detect secret patterns
        self.assertIsInstance(secrets, list, "Should return list of potential secrets")
        
        # Check secret detection
        if secrets:
            for secret in secrets:
                self.assertIn('type', secret, "Should identify secret type")
                self.assertIn('line', secret, "Should include line number")
                self.assertIn('value_preview', secret, "Should include value preview")
    
    def test_file_permissions_check(self):
        """Test checking for insecure file permissions"""
        # Create files with different permissions
        secure_file = self.create_test_file("secure.txt", "secure content")
        config_file = self.create_test_file("config.conf", "configuration data")
        
        from maintenance_agent import SecurityScanner
        scanner = SecurityScanner()
        perm_issues = scanner.check_file_permissions(str(self.temp_path))
        
        # Should analyze file permissions
        self.assertIsInstance(perm_issues, list, "Should return permission issues list")
        
        # Check structure
        for issue in perm_issues:
            self.assertIn('file', issue, "Should include file path")
            self.assertIn('current_permissions', issue, "Should include current permissions")
            self.assertIn('recommended_permissions', issue, "Should include recommendations")


class TestProjectHealthMonitoring(unittest.TestCase):
    """Test project health monitoring capabilities"""
    
    def setUp(self):
        """Set up test files"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        """Clean up test files"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, filename, content):
        """Create a test file"""
        file_path = self.temp_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return file_path
    
    def test_code_quality_metrics(self):
        """Test calculation of code quality metrics"""
        python_code = '''
def calculate_metrics():
    """Calculate code quality metrics"""
    # This is a well-documented function
    lines_of_code = 100
    comments = 20
    functions = 10
    
    complexity = 5  # Cyclomatic complexity
    
    return {
        'loc': lines_of_code,
        'comments': comments,
        'functions': functions,
        'complexity': complexity
    }

class MetricsCalculator:
    """A class for calculating metrics"""
    
    def __init__(self):
        self.data = {}
    
    def process(self, input_data):
        # Process the input data
        if not input_data:
            return None
        
        result = []
        for item in input_data:
            processed_item = self._process_item(item)
            result.append(processed_item)
        
        return result
    
    def _process_item(self, item):
        return item.upper()
'''
        
        file_path = self.create_test_file("quality_code.py", python_code)
        
        from maintenance_agent import ProjectHealthMonitor
        monitor = ProjectHealthMonitor()
        metrics = monitor.calculate_code_quality_metrics(str(file_path))
        
        # Should calculate various metrics
        self.assertIn('lines_of_code', metrics, "Should calculate lines of code")
        self.assertIn('comment_ratio', metrics, "Should calculate comment ratio")
        self.assertIn('function_count', metrics, "Should count functions")
        self.assertIn('class_count', metrics, "Should count classes")
        self.assertGreater(metrics['lines_of_code'], 0, "Should have positive LOC")
    
    def test_test_coverage_analysis(self):
        """Test analysis of test coverage"""
        test_file_content = '''
import unittest

class TestExample(unittest.TestCase):
    
    def test_addition(self):
        self.assertEqual(2 + 2, 4)
    
    def test_subtraction(self):
        self.assertEqual(5 - 3, 2)
    
    def test_multiplication(self):
        self.assertEqual(3 * 4, 12)

if __name__ == "__main__":
    unittest.main()
'''
        
        source_file_content = '''
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    # This function is not tested
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
'''
        
        self.create_test_file("test_math.py", test_file_content)
        self.create_test_file("math_utils.py", source_file_content)
        
        from maintenance_agent import ProjectHealthMonitor
        monitor = ProjectHealthMonitor()
        coverage = monitor.analyze_test_coverage(str(self.temp_path))
        
        # Should provide coverage analysis
        self.assertIn('test_files_found', coverage, "Should count test files")
        self.assertIn('source_files_found', coverage, "Should count source files")
        self.assertIn('coverage_estimate', coverage, "Should estimate coverage")
    
    def test_project_structure_validation(self):
        """Test validation of project structure"""
        # Create a typical project structure
        self.create_test_file("README.md", "# Project README")
        self.create_test_file("requirements.txt", "pandas==1.5.3")
        self.create_test_file(".gitignore", "__pycache__/")
        self.create_test_file("src/main.py", "print('Hello World')")
        self.create_test_file("tests/test_main.py", "import unittest")
        self.create_test_file("docs/api.md", "# API Documentation")
        
        from maintenance_agent import ProjectHealthMonitor
        monitor = ProjectHealthMonitor()
        structure = monitor.validate_project_structure(str(self.temp_path))
        
        # Should analyze project structure
        self.assertIn('has_readme', structure, "Should check for README")
        self.assertIn('has_requirements', structure, "Should check for requirements")
        self.assertIn('has_gitignore', structure, "Should check for gitignore")
        self.assertIn('has_tests', structure, "Should check for tests")
        self.assertIn('has_docs', structure, "Should check for documentation")
        
        # Check boolean results
        self.assertTrue(structure['has_readme'], "Should find README file")
        self.assertTrue(structure['has_requirements'], "Should find requirements file")
    
    def test_git_repository_health(self):
        """Test analysis of git repository health"""
        from maintenance_agent import ProjectHealthMonitor
        monitor = ProjectHealthMonitor()
        
        # Test with current repository (if it exists)
        repo_health = monitor.analyze_git_health(".")
        
        # Should provide git analysis
        self.assertIn('is_git_repo', repo_health, "Should check if git repository")
        self.assertIn('has_remote', repo_health, "Should check for remote")
        self.assertIn('branch_info', repo_health, "Should provide branch info")


class TestMaintenanceReporting(unittest.TestCase):
    """Test maintenance reporting and recommendations"""
    
    def test_maintenance_report_generation(self):
        """Test generation of comprehensive maintenance report"""
        from maintenance_agent import MaintenanceReporter
        reporter = MaintenanceReporter()
        
        # Mock data for report generation
        mock_data = {
            'dependencies': [
                {'name': 'pandas', 'version': '1.5.3', 'latest': '2.0.0', 'outdated': True},
                {'name': 'numpy', 'version': '1.24.3', 'latest': '1.24.3', 'outdated': False}
            ],
            'security_issues': [
                {'type': 'vulnerability', 'severity': 'medium', 'package': 'requests'}
            ],
            'code_quality': {
                'lines_of_code': 1500,
                'comment_ratio': 0.15,
                'function_count': 45
            }
        }
        
        report = reporter.generate_maintenance_report(mock_data)
        
        # Should generate comprehensive report
        self.assertIn('summary', report, "Should include summary")
        self.assertIn('dependencies', report, "Should include dependency analysis")
        self.assertIn('security', report, "Should include security analysis")
        self.assertIn('code_quality', report, "Should include quality metrics")
        self.assertIn('recommendations', report, "Should include recommendations")
    
    def test_priority_recommendations(self):
        """Test generation of priority-based recommendations"""
        from maintenance_agent import MaintenanceReporter
        reporter = MaintenanceReporter()
        
        # Mock issues with different priorities
        issues = [
            {'type': 'security', 'severity': 'high', 'description': 'Critical vulnerability'},
            {'type': 'dependency', 'severity': 'medium', 'description': 'Outdated package'},
            {'type': 'quality', 'severity': 'low', 'description': 'Code formatting'}
        ]
        
        recommendations = reporter.prioritize_recommendations(issues)
        
        # Should prioritize by severity
        self.assertIsInstance(recommendations, list, "Should return list of recommendations")
        self.assertGreater(len(recommendations), 0, "Should generate recommendations")
        
        # Check structure
        for rec in recommendations:
            self.assertIn('priority', rec, "Should include priority level")
            self.assertIn('action', rec, "Should include recommended action")
            self.assertIn('description', rec, "Should include description")


class TestMaintenanceIntegration(unittest.TestCase):
    """Test integration with the agent framework"""
    
    def test_agent_configuration(self):
        """Test that the maintenance agent configuration is valid"""
        from agent_config_parser import AgentConfigParser
        
        # Use absolute path to configurations directory
        config_dir = Path(__file__).parent / "configurations"
        parser = AgentConfigParser(str(config_dir))
        agents = parser.load_all_agents()
        config = parser.get_agent_config("maintenance-agent")
        
        self.assertIsNotNone(config, "Maintenance agent configuration should exist")
        self.assertEqual(config['name'], "maintenance-agent")
        self.assertEqual(config['specialization'], "project-maintenance-and-monitoring")
    
    def test_security_integration(self):
        """Test that the maintenance agent works with security framework"""
        from security_framework import SecurityFramework, PermissionType
        from agent_config_parser import AgentConfigParser
        
        # Use absolute path to configurations directory
        config_dir = Path(__file__).parent / "configurations"
        parser = AgentConfigParser(str(config_dir))
        agents = parser.load_all_agents()
        config = parser.get_agent_config("maintenance-agent")
        
        framework = SecurityFramework()
        session_id = framework.create_session("maintenance-agent", config)
        
        # Test permissions
        can_read_requirements = framework.check_permission(
            session_id, PermissionType.READ, "requirements.txt", config
        )
        can_write_reports = framework.check_permission(
            session_id, PermissionType.WRITE, "generated-content/maintenance-report.md", config
        )
        
        self.assertTrue(can_read_requirements, "Should be able to read requirements files")
        self.assertTrue(can_write_reports, "Should be able to write maintenance reports")
        
        framework.end_session(session_id)


def run_tests():
    """Run all maintenance agent tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestDependencyMonitoring,
        TestSecurityScanning,
        TestProjectHealthMonitoring,
        TestMaintenanceReporting,
        TestMaintenanceIntegration
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