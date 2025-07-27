#!/usr/bin/env python3
"""
Basic Sub-Agents Usage Examples
Demonstrates common sub-agent operations and workflows
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from integration_handler import ClaudeCodeIntegration, ResultFormatter, ProgressDisplay


def example_list_agents():
    """Example: List all available agents"""
    print("=== Listing Available Agents ===")
    
    integration = ClaudeCodeIntegration()
    result = integration.execute_command('list-agents', {})
    
    if result.get('status') == 'success':
        agents = result.get('agents', [])
        print(f"Found {len(agents)} agents:")
        
        for agent in agents:
            print(f"  • {agent['name']}: {agent['specialization']}")
            print(f"    Status: {agent['status']}, Version: {agent['version']}")
            capabilities = agent.get('capabilities', [])
            if capabilities:
                print(f"    Capabilities: {', '.join(capabilities)}")
            print()
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def example_run_single_agent():
    """Example: Run a single agent"""
    print("=== Running Code Quality Agent ===")
    
    integration = ClaudeCodeIntegration()
    
    # Run code quality analysis
    result = integration.execute_command('run-agent', {
        'agent': 'code-quality-agent',
        'action': 'analyze',
        'target': '*.py'
    })
    
    # Format and display results
    formatter = ResultFormatter()
    if result.get('status') == 'success':
        formatted = formatter.format_agent_result(result)
        print(formatted)
    else:
        error_formatted = formatter.format_error_result(result)
        print(error_formatted)


def example_agent_status():
    """Example: Check agent status"""
    print("=== Checking Agent Status ===")
    
    integration = ClaudeCodeIntegration()
    
    agents_to_check = ['code-quality-agent', 'documentation-agent', 'maintenance-agent']
    
    for agent_name in agents_to_check:
        result = integration.execute_command('agent-status', {'agent': agent_name})
        
        if result.get('status') == 'success':
            print(f"Agent: {agent_name}")
            print(f"  Status: {result.get('status')}")
            print(f"  Specialization: {result.get('specialization', 'Unknown')}")
            print(f"  Version: {result.get('version', 'Unknown')}")
            print(f"  Last Execution: {result.get('last_execution', 'N/A')}")
        else:
            print(f"Agent {agent_name}: {result.get('error', 'Status unknown')}")
        print()


def example_run_workflow():
    """Example: Execute a predefined workflow"""
    print("=== Running Code Quality Workflow ===")
    
    integration = ClaudeCodeIntegration()
    
    # Start workflow execution
    result = integration.execute_command('run-workflow', {
        'workflow': 'code-quality-check',
        'context': {'project_path': '.'}
    })
    
    # Format and display workflow results
    formatter = ResultFormatter()
    if result.get('status') in ['completed', 'partial_failure']:
        formatted = formatter.format_workflow_result(result)
        print(formatted)
        
        # Show any errors
        errors = result.get('errors', [])
        if errors:
            print("\n⚠️ Issues encountered:")
            for error in errors:
                print(f"  • {error.get('message', 'Unknown error')}")
    else:
        error_formatted = formatter.format_error_result(result)
        print(error_formatted)


def example_progress_monitoring():
    """Example: Demonstrate progress monitoring"""
    print("=== Progress Monitoring Example ===")
    
    display = ProgressDisplay()
    
    # Simulate workflow progress
    display.start_workflow('example-workflow', 3)
    
    print("Initial state:")
    print(display.get_current_display())
    
    # Simulate agent progress updates
    import time
    
    print("\nUpdating progress...")
    display.update_agent_progress('code-quality-agent', 'running', 30)
    print(display.get_current_display())
    
    time.sleep(1)
    
    display.update_agent_progress('code-quality-agent', 'completed', 100)
    display.update_agent_progress('documentation-agent', 'running', 50)
    print(display.get_current_display())
    
    time.sleep(1)
    
    display.update_agent_progress('documentation-agent', 'completed', 100)
    display.update_agent_progress('maintenance-agent', 'running', 75)
    print(display.get_current_display())


def example_custom_configuration():
    """Example: Custom agent configuration"""
    print("=== Custom Configuration Example ===")
    
    from integration_handler import ConfigurationManager
    
    config_manager = ConfigurationManager()
    
    # Create a custom workflow
    success = config_manager.create_custom_workflow(
        name='documentation-update',
        agents=['documentation-agent', 'content-generation-agent'],
        execution_type='sequential'
    )
    
    if success:
        print("✅ Created custom workflow: documentation-update")
        
        # List all workflows including the new one
        workflows = config_manager.list_available_workflows()
        print(f"\nAvailable workflows ({len(workflows)}):")
        for workflow in workflows:
            print(f"  • {workflow['name']} ({workflow['type']})")
    else:
        print("❌ Failed to create custom workflow")


def main():
    """Run all examples"""
    print("Sub-Agents System Examples")
    print("=" * 50)
    
    examples = [
        example_list_agents,
        example_agent_status,
        example_run_single_agent,
        example_run_workflow,
        example_progress_monitoring,
        example_custom_configuration
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            print(f"\n{i}. {example_func.__doc__.split(':')[1].strip()}")
            print("-" * 30)
            example_func()
        except Exception as e:
            print(f"Error running example: {e}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")


if __name__ == "__main__":
    main()