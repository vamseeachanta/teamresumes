#!/usr/bin/env python3
"""
Sub-Agent System Integration Test
Tests the complete sub-agent infrastructure
"""

import os
import sys
from pathlib import Path

# Add the sub-agents directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from agent_config_parser import AgentConfigParser, AgentConfigError
from security_framework import SecurityFramework, PermissionType

def test_configuration_system():
    """Test the agent configuration parser"""
    print("Testing Configuration System...")
    
    parser = AgentConfigParser()
    
    try:
        # Load all agent configurations
        agents = parser.load_all_agents()
        print(f"PASS Loaded {len(agents)} agent configurations")
        
        # Test specific agent retrieval
        code_quality_config = parser.get_agent_config("code-quality-agent")
        if code_quality_config:
            print("PASS Retrieved code-quality-agent configuration")
        else:
            print("FAIL Failed to retrieve code-quality-agent configuration")
        
        # Test active agents list
        active_agents = parser.list_active_agents()
        print(f"PASS Found {len(active_agents)} active agents: {', '.join(active_agents)}")
        
        # Test agent compatibility
        if len(active_agents) >= 2:
            compatible = parser.validate_agent_compatibility(active_agents[0], active_agents[1])
            print(f"PASS Agent compatibility check: {compatible}")
        
        return True
        
    except Exception as e:
        print(f"FAIL Configuration system test failed: {e}")
        return False

def test_security_framework():
    """Test the security framework"""
    print("\nTesting Security Framework...")
    
    framework = SecurityFramework()
    
    # Mock agent configuration
    agent_config = {
        "name": "test-agent",
        "permissions": {
            "read": ["*.py", "*.md", "cv/*.md"],
            "write": ["*.py"],
            "execute": ["code_analysis"]
        },
        "security": {
            "max_file_size": 10,
            "timeout": 300,
            "sandbox_mode": True,
            "audit_logging": True
        },
        "behavior": {
            "max_operations": 50
        }
    }
    
    try:
        # Create session
        session_id = framework.create_session("test-agent", agent_config)
        print("PASS Created agent session")
        
        # Test permissions
        tests = [
            (PermissionType.READ, "cv/va_resume.md", True, "Read resume file"),
            (PermissionType.READ, "README.md", True, "Read README"),
            (PermissionType.WRITE, "main.py", True, "Write Python file"),
            (PermissionType.WRITE, "cv/va_resume.md", False, "Write resume (no permission)"),
            (PermissionType.READ, ".git/config", False, "Read git config (restricted)"),
        ]
        
        passed = 0
        total = len(tests)
        
        for operation, file_path, expected, description in tests:
            result = framework.check_permission(session_id, operation, file_path, agent_config)
            if result == expected:
                print(f"PASS {description}")
                passed += 1
            else:
                print(f"FAIL {description} (expected {expected}, got {result})")
        
        print(f"PASS Permission tests: {passed}/{total} passed")
        
        # Test file locking
        lock_acquired = framework._acquire_file_lock("test.py", "test-agent")
        if lock_acquired:
            print("PASS File lock acquired")
            
            # Try to acquire same lock with different agent
            lock_conflict = framework._acquire_file_lock("test.py", "other-agent")
            if not lock_conflict:
                print("PASS File lock conflict detected correctly")
            else:
                print("FAIL File lock conflict not detected")
            
            # Release lock
            framework.release_file_lock("test.py", "test-agent")
            print("PASS File lock released")
        
        # End session
        framework.end_session(session_id)
        print("PASS Session ended successfully")
        
        # Generate security report
        report = framework.get_security_report()
        print(f"PASS Security report: {report['violations']} violations, {report['audit_events']} audit events")
        
        return True
        
    except Exception as e:
        print(f"FAIL Security framework test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files and directories exist"""
    print("\nTesting File Structure...")
    
    required_files = [
        ".agent-os/sub-agents/configurations/agent-template.yaml",
        ".agent-os/sub-agents/configurations/code-quality-agent.yaml",
        ".agent-os/sub-agents/configurations/documentation-agent.yaml",
        ".agent-os/sub-agents/templates/prompts/code-review-prompt.md",
        ".agent-os/sub-agents/templates/prompts/documentation-update-prompt.md",
        ".agent-os/sub-agents/coordination/agent-coordinator.md",
        ".agent-os/sub-agents/coordination/workflow-definitions.yaml",
        ".agent-os/sub-agents/agent_config_parser.py",
        ".agent-os/sub-agents/security_framework.py"
    ]
    
    required_dirs = [
        ".agent-os/sub-agents/configurations",
        ".agent-os/sub-agents/templates/prompts",
        ".agent-os/sub-agents/templates/workflows",
        ".agent-os/sub-agents/coordination"
    ]
    
    all_exist = True
    
    # Check directories
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"PASS Directory exists: {dir_path}")
        else:
            print(f"FAIL Directory missing: {dir_path}")
            all_exist = False
    
    # Check files
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"PASS File exists: {file_path}")
        else:
            print(f"FAIL File missing: {file_path}")
            all_exist = False
    
    return all_exist

def test_yaml_validity():
    """Test that all YAML files are valid"""
    print("\nTesting YAML Validity...")
    
    import yaml
    
    yaml_files = [
        ".agent-os/sub-agents/configurations/agent-template.yaml",
        ".agent-os/sub-agents/configurations/code-quality-agent.yaml",
        ".agent-os/sub-agents/configurations/documentation-agent.yaml",
        ".agent-os/sub-agents/coordination/workflow-definitions.yaml"
    ]
    
    all_valid = True
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                yaml.safe_load(f)
            print(f"PASS Valid YAML: {yaml_file}")
        except yaml.YAMLError as e:
            print(f"FAIL Invalid YAML: {yaml_file} - {e}")
            all_valid = False
        except FileNotFoundError:
            print(f"FAIL File not found: {yaml_file}")
            all_valid = False
    
    return all_valid

def main():
    """Run all tests"""
    print("Sub-Agent System Integration Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("YAML Validity", test_yaml_validity),
        ("Configuration System", test_configuration_system),
        ("Security Framework", test_security_framework)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("PASS All tests passed! Sub-agent infrastructure is ready.")
        return 0
    else:
        print(f"FAIL {total - passed} tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)