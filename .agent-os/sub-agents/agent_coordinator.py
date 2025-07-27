#!/usr/bin/env python3
"""
Agent Coordinator - Multi-agent orchestration and workflow management
Handles coordination of multiple sub-agents with sequential/parallel execution and conditional logic
"""

import os
import sys
import yaml
import json
import asyncio
import threading
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowParser:
    """Parses and validates workflow definition files"""
    
    def __init__(self):
        self.supported_versions = ['1.0.0', '1.1.0']
    
    def parse_workflow(self, workflow_file: str) -> Dict[str, Any]:
        """Parse workflow from YAML file"""
        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_data = yaml.safe_load(f)
            
            # Validate basic structure
            validator = WorkflowValidator()
            is_valid, errors = validator.validate_workflow(workflow_data)
            
            if not is_valid:
                raise ValueError(f"Invalid workflow: {', '.join(errors)}")
            
            # Add metadata
            workflow_data['source_file'] = workflow_file
            workflow_data['parsed_at'] = datetime.now().isoformat()
            
            return workflow_data
            
        except FileNotFoundError:
            logger.error(f"Workflow file not found: {workflow_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in workflow file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error parsing workflow: {e}")
            raise
    
    def parse_workflow_dict(self, workflow_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Parse workflow from dictionary"""
        # Validate structure
        validator = WorkflowValidator()
        is_valid, errors = validator.validate_workflow(workflow_dict)
        
        if not is_valid:
            raise ValueError(f"Invalid workflow: {', '.join(errors)}")
        
        # Add metadata
        workflow_dict['parsed_at'] = datetime.now().isoformat()
        
        return workflow_dict


class WorkflowValidator:
    """Validates workflow definitions for correctness"""
    
    REQUIRED_FIELDS = ['name', 'agents', 'steps']
    OPTIONAL_FIELDS = ['version', 'description', 'execution', 'context']
    
    def validate_workflow(self, workflow: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate workflow structure and dependencies"""
        errors = []
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in workflow:
                errors.append(f"Missing required field: {field}")
        
        # Validate agents list
        if 'agents' in workflow:
            if not isinstance(workflow['agents'], list) or len(workflow['agents']) == 0:
                errors.append("'agents' must be a non-empty list")
        
        # Validate steps
        if 'steps' in workflow:
            if not isinstance(workflow['steps'], list) or len(workflow['steps']) == 0:
                errors.append("'steps' must be a non-empty list")
            else:
                step_errors = self._validate_steps(workflow['steps'])
                errors.extend(step_errors)
        
        # Validate execution configuration
        if 'execution' in workflow:
            exec_errors = self._validate_execution_config(workflow['execution'])
            errors.extend(exec_errors)
        
        return len(errors) == 0, errors
    
    def _validate_steps(self, steps: List[Dict[str, Any]]) -> List[str]:
        """Validate workflow steps"""
        errors = []
        
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"Step {i} must be a dictionary")
                continue
            
            # Check for required fields in step
            if 'agent' not in step and 'group' not in step:
                errors.append(f"Step {i} must have either 'agent' or 'group' field")
            
            # Validate dependencies
            if 'depends_on' in step:
                if not isinstance(step['depends_on'], (str, list)):
                    errors.append(f"Step {i} 'depends_on' must be string or list")
            
            # Validate conditions
            if 'condition' in step:
                if not isinstance(step['condition'], str):
                    errors.append(f"Step {i} 'condition' must be a string")
        
        return errors
    
    def _validate_execution_config(self, execution: Dict[str, Any]) -> List[str]:
        """Validate execution configuration"""
        errors = []
        
        valid_types = ['sequential', 'parallel', 'mixed']
        if 'type' in execution:
            if execution['type'] not in valid_types:
                errors.append(f"Invalid execution type. Must be one of: {valid_types}")
        
        if execution.get('type') == 'parallel':
            if 'max_concurrent' in execution:
                if not isinstance(execution['max_concurrent'], int) or execution['max_concurrent'] < 1:
                    errors.append("'max_concurrent' must be a positive integer")
        
        return errors


class AgentCoordinator:
    """Coordinates execution of multiple sub-agents"""
    
    def __init__(self, config_parser=None, security_framework=None):
        self.config_parser = config_parser
        self.security_framework = security_framework
        self.active_sessions = {}
        self.workflow_context = {}
        self.execution_history = []
        
        # Import agent modules dynamically
        self._load_agent_modules()
    
    def _load_agent_modules(self):
        """Dynamically load agent modules"""
        self.agent_modules = {}
        
        # Get current directory to find agent modules
        current_dir = Path(__file__).parent
        
        agent_files = [
            'code_quality_agent.py',
            'documentation_agent.py', 
            'resume_processing_agent.py',
            'content_generation_agent.py',
            'maintenance_agent.py'
        ]
        
        for agent_file in agent_files:
            agent_path = current_dir / agent_file
            if agent_path.exists():
                agent_name = agent_file.replace('.py', '').replace('_', '-')
                try:
                    # Import the module
                    module_name = agent_file.replace('.py', '')
                    module = __import__(module_name)
                    self.agent_modules[agent_name] = module
                    logger.info(f"Loaded agent module: {agent_name}")
                except ImportError as e:
                    logger.warning(f"Could not load agent module {agent_name}: {e}")
    
    def discover_agents(self) -> List[Dict[str, Any]]:
        """Discover available agents from configuration"""
        available_agents = []
        
        if self.config_parser:
            try:
                agents = self.config_parser.load_all_agents()
                for agent_name, config in agents.items():
                    agent_info = {
                        'name': agent_name,
                        'specialization': config.get('specialization', 'unknown'),
                        'status': config.get('metadata', {}).get('status', 'active'),
                        'capabilities': config.get('metadata', {}).get('capabilities', []),
                        'version': config.get('version', '1.0.0')
                    }
                    available_agents.append(agent_info)
            except Exception as e:
                logger.error(f"Error discovering agents: {e}")
        
        return available_agents
    
    def set_security_framework(self, security_framework):
        """Set the security framework for agent execution"""
        self.security_framework = security_framework
    
    def execute_workflow(self, workflow: Dict[str, Any], 
                        status_callback: Optional[Callable] = None,
                        context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a workflow with multiple agents"""
        
        workflow_id = f"workflow_{int(time.time())}"
        start_time = datetime.now()
        
        # Initialize execution context
        execution_context = {
            'workflow_id': workflow_id,
            'workflow_name': workflow.get('name', 'unnamed'),
            'start_time': start_time,
            'context': context or workflow.get('context', {}),
            'shared_data': {},
            'agent_results': [],
            'errors': []
        }
        
        # Update status
        if status_callback:
            status_callback('initializing')
        
        try:
            # Get execution configuration
            execution_config = workflow.get('execution', {'type': 'sequential'})
            execution_type = execution_config.get('type', 'sequential')
            
            if status_callback:
                status_callback('running')
            
            # Execute based on type
            if execution_type == 'sequential':
                self._execute_sequential(workflow, execution_context)
            elif execution_type == 'parallel':
                self._execute_parallel(workflow, execution_context)
            elif execution_type == 'mixed':
                self._execute_mixed(workflow, execution_context)
            else:
                raise ValueError(f"Unknown execution type: {execution_type}")
            
            # Determine final status
            if execution_context['errors']:
                final_status = 'partial_failure' if execution_context['agent_results'] else 'failed'
            else:
                final_status = 'completed'
            
            if status_callback:
                status_callback(final_status)
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            execution_context['errors'].append({
                'type': 'workflow_error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            })
            final_status = 'failed'
            
            if status_callback:
                status_callback('failed')
        
        # Compile final results
        end_time = datetime.now()
        execution_duration = (end_time - start_time).total_seconds()
        
        results = {
            'workflow_id': workflow_id,
            'workflow_name': execution_context['workflow_name'],
            'status': final_status,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': execution_duration,
            'agent_results': execution_context['agent_results'],
            'errors': execution_context['errors'],
            'shared_data': execution_context['shared_data']
        }
        
        # Store in execution history
        self.execution_history.append(results)
        
        return results
    
    def _execute_sequential(self, workflow: Dict[str, Any], context: Dict[str, Any]):
        """Execute workflow steps sequentially"""
        steps = workflow.get('steps', [])
        
        for i, step in enumerate(steps):
            try:
                # Check if step should be executed
                if not self._should_execute_step(step, context):
                    logger.info(f"Skipping step {i} due to condition")
                    continue
                
                # Execute step
                if 'agent' in step:
                    # Single agent step
                    result = self._execute_single_agent_step(step, context)
                    context['agent_results'].append(result)
                    
                    # Check if agent execution failed
                    if result.get('status') == 'error':
                        context['errors'].append({
                            'step': i,
                            'agent': result.get('agent', 'unknown'),
                            'type': 'agent_error',
                            'message': result.get('error', 'Unknown agent error'),
                            'timestamp': datetime.now().isoformat()
                        })
                    
                    # Update shared data
                    if 'output_key' in step and result.get('status') == 'success':
                        output_key = step['output_key']
                        context['shared_data'][output_key] = result.get('results', {})
                
                elif 'group' in step:
                    # Group step (could be parallel within sequential)
                    group_results = self._execute_group_step(step, context)
                    context['agent_results'].extend(group_results)
                
            except Exception as e:
                logger.error(f"Error executing step {i}: {e}")
                context['errors'].append({
                    'step': i,
                    'type': 'step_error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    def _execute_parallel(self, workflow: Dict[str, Any], context: Dict[str, Any]):
        """Execute workflow steps in parallel"""
        steps = workflow.get('steps', [])
        max_concurrent = workflow.get('execution', {}).get('max_concurrent', len(steps))
        
        # Filter steps that should be executed
        executable_steps = []
        for i, step in enumerate(steps):
            if self._should_execute_step(step, context):
                executable_steps.append((i, step))
            else:
                logger.info(f"Skipping step {i} due to condition")
        
        # Execute steps in parallel
        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            # Submit all steps
            future_to_step = {}
            for step_index, step in executable_steps:
                if 'agent' in step:
                    future = executor.submit(self._execute_single_agent_step, step, context)
                    future_to_step[future] = (step_index, step)
            
            # Collect results
            for future in as_completed(future_to_step):
                step_index, step = future_to_step[future]
                try:
                    result = future.result()
                    context['agent_results'].append(result)
                    
                    # Update shared data
                    if 'output_key' in step and result.get('status') == 'success':
                        output_key = step['output_key']
                        context['shared_data'][output_key] = result.get('results', {})
                        
                except Exception as e:
                    logger.error(f"Error in parallel step {step_index}: {e}")
                    context['errors'].append({
                        'step': step_index,
                        'type': 'parallel_step_error',
                        'message': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
    
    def _execute_mixed(self, workflow: Dict[str, Any], context: Dict[str, Any]):
        """Execute workflow with mixed sequential/parallel steps"""
        steps = workflow.get('steps', [])
        
        for i, step in enumerate(steps):
            try:
                if not self._should_execute_step(step, context):
                    logger.info(f"Skipping step {i} due to condition")
                    continue
                
                if step.get('parallel', False):
                    # Execute this step and any subsequent parallel steps together
                    parallel_steps = [step]
                    j = i + 1
                    while j < len(steps) and steps[j].get('parallel', False):
                        if self._should_execute_step(steps[j], context):
                            parallel_steps.append(steps[j])
                        j += 1
                    
                    # Execute parallel group
                    self._execute_parallel_group(parallel_steps, context)
                    
                    # Skip the parallel steps we just executed
                    i = j - 1
                else:
                    # Execute sequentially
                    if 'agent' in step:
                        result = self._execute_single_agent_step(step, context)
                        context['agent_results'].append(result)
                        
                        if 'output_key' in step and result.get('status') == 'success':
                            output_key = step['output_key']
                            context['shared_data'][output_key] = result.get('results', {})
                
            except Exception as e:
                logger.error(f"Error executing mixed step {i}: {e}")
                context['errors'].append({
                    'step': i,
                    'type': 'mixed_step_error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    def _execute_parallel_group(self, steps: List[Dict[str, Any]], context: Dict[str, Any]):
        """Execute a group of steps in parallel"""
        max_workers = min(len(steps), 5)  # Limit concurrent execution
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_step = {}
            for step in steps:
                if 'agent' in step:
                    future = executor.submit(self._execute_single_agent_step, step, context)
                    future_to_step[future] = step
            
            # Collect results
            for future in as_completed(future_to_step):
                step = future_to_step[future]
                try:
                    result = future.result()
                    context['agent_results'].append(result)
                    
                    if 'output_key' in step and result.get('status') == 'success':
                        output_key = step['output_key']
                        context['shared_data'][output_key] = result.get('results', {})
                        
                except Exception as e:
                    logger.error(f"Error in parallel group step: {e}")
                    context['errors'].append({
                        'type': 'parallel_group_error',
                        'message': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
    
    def _execute_group_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute a group step (could contain multiple agents)"""
        group_results = []
        
        if step.get('parallel', False):
            # Execute group agents in parallel
            agents = step.get('agents', [])
            max_workers = min(len(agents), 5)
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_agent = {}
                for agent_step in agents:
                    future = executor.submit(self._execute_single_agent_step, agent_step, context)
                    future_to_agent[future] = agent_step
                
                for future in as_completed(future_to_agent):
                    agent_step = future_to_agent[future]
                    try:
                        result = future.result()
                        group_results.append(result)
                    except Exception as e:
                        logger.error(f"Error in group agent execution: {e}")
                        error_result = {
                            'agent': agent_step.get('agent', 'unknown'),
                            'status': 'error',
                            'error': str(e),
                            'timestamp': datetime.now().isoformat()
                        }
                        group_results.append(error_result)
        else:
            # Execute group agents sequentially
            agents = step.get('agents', [])
            for agent_step in agents:
                try:
                    result = self._execute_single_agent_step(agent_step, context)
                    group_results.append(result)
                except Exception as e:
                    logger.error(f"Error in group agent execution: {e}")
                    error_result = {
                        'agent': agent_step.get('agent', 'unknown'),
                        'status': 'error',
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    }
                    group_results.append(error_result)
        
        return group_results
    
    def _execute_single_agent_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single agent step"""
        agent_name = step.get('agent')
        action = step.get('action', 'default')
        parameters = step.get('parameters', {})
        
        # Add shared context to parameters
        if context.get('context'):
            parameters['context'] = context['context']
        
        # Add input data from previous agents
        if 'input_from' in step:
            input_key = step['input_from']
            if input_key in context['shared_data']:
                parameters[input_key] = context['shared_data'][input_key]
        
        # Execute the agent
        start_time = datetime.now()
        try:
            result = self._execute_agent(agent_name, action, parameters)
            result['agent'] = agent_name
            result['action'] = action
            result['start_time'] = start_time.isoformat()
            result['end_time'] = datetime.now().isoformat()
            result['duration'] = (datetime.now() - start_time).total_seconds()
            
            return result
            
        except Exception as e:
            logger.error(f"Error executing agent {agent_name}: {e}")
            return {
                'agent': agent_name,
                'action': action,
                'status': 'error',
                'error': str(e),
                'start_time': start_time.isoformat(),
                'end_time': datetime.now().isoformat()
            }
    
    def _execute_agent(self, agent_name: str, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific agent with given parameters"""
        
        # Create security session if framework is available
        session_id = None
        if self.security_framework and self.config_parser:
            try:
                config = self.config_parser.get_agent_config(agent_name)
                if config:
                    session_id = self.security_framework.create_session(agent_name, config)
            except Exception as e:
                logger.warning(f"Could not create security session for {agent_name}: {e}")
        
        try:
            # Mock agent execution for now
            # In a real implementation, this would instantiate and run the actual agent
            
            # Simulate different agent behaviors
            if agent_name == 'code-quality-agent':
                return {
                    'status': 'success',
                    'results': {
                        'quality_score': 85,
                        'issues_found': 3,
                        'recommendations': ['Add more comments', 'Reduce complexity']
                    }
                }
            elif agent_name == 'documentation-agent':
                return {
                    'status': 'success',
                    'results': {
                        'docs_updated': True,
                        'files_processed': 5,
                        'links_checked': 12
                    }
                }
            elif agent_name == 'maintenance-agent':
                return {
                    'status': 'success',
                    'results': {
                        'dependencies_checked': 15,
                        'vulnerabilities_found': 1,
                        'updates_available': 3
                    }
                }
            else:
                # Generic success response
                return {
                    'status': 'success',
                    'results': {
                        'action_completed': action,
                        'timestamp': datetime.now().isoformat()
                    }
                }
                
        finally:
            # Clean up security session
            if session_id and self.security_framework:
                try:
                    self.security_framework.end_session(session_id)
                except Exception as e:
                    logger.warning(f"Error ending security session: {e}")
    
    def _should_execute_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Determine if a step should be executed based on conditions"""
        
        # Check dependencies
        if 'depends_on' in step:
            depends_on = step['depends_on']
            if isinstance(depends_on, str):
                depends_on = [depends_on]
            
            # Check if all dependencies have completed successfully
            completed_agents = {result['agent'] for result in context['agent_results'] 
                              if result.get('status') == 'success'}
            
            for dependency in depends_on:
                if dependency not in completed_agents:
                    logger.info(f"Step dependency not met: {dependency}")
                    return False
        
        # Check conditions
        if 'condition' in step:
            condition = step['condition']
            try:
                # Simple condition evaluation
                # In a real implementation, this would be more sophisticated
                return self._evaluate_condition(condition, context)
            except Exception as e:
                logger.warning(f"Error evaluating condition '{condition}': {e}")
                return True  # Default to executing if condition evaluation fails
        
        return True
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a condition string against the current context"""
        
        # Simple condition evaluation
        # This is a basic implementation - a real system would use a proper expression parser
        
        # Extract variables from shared data
        variables = context.get('shared_data', {})
        
        # Handle simple numeric comparisons
        if '<' in condition:
            left, right = condition.split('<', 1)
            left_val = self._extract_value(left.strip(), variables)
            right_val = self._extract_value(right.strip(), variables)
            return float(left_val) < float(right_val)
        
        elif '>' in condition:
            left, right = condition.split('>', 1)
            left_val = self._extract_value(left.strip(), variables)
            right_val = self._extract_value(right.strip(), variables)
            return float(left_val) > float(right_val)
        
        elif '==' in condition:
            left, right = condition.split('==', 1)
            left_val = self._extract_value(left.strip(), variables)
            right_val = self._extract_value(right.strip(), variables)
            return str(left_val) == str(right_val)
        
        # Default evaluation
        return True
    
    def _extract_value(self, expression: str, variables: Dict[str, Any]) -> Any:
        """Extract value from expression using available variables"""
        
        # Remove quotes if present
        expression = expression.strip('\'"')
        
        # Check if it's a number
        try:
            return float(expression)
        except ValueError:
            pass
        
        # Check if it's a variable (exact match)
        if expression in variables:
            var_value = variables[expression]
            # If the variable contains a dict with the same key, return the inner value
            if isinstance(var_value, dict) and expression in var_value:
                return var_value[expression]
            return var_value
        
        # Check for nested access across all variables
        for var_name, var_value in variables.items():
            if isinstance(var_value, dict) and expression in var_value:
                return var_value[expression]
        
        # Return as string if nothing else matches
        return expression


class WorkflowManager:
    """Manages workflow definitions and lifecycle"""
    
    def __init__(self):
        self.workflows = {}
        self.workflow_history = []
    
    def register_workflow(self, name: str, workflow: Dict[str, Any]):
        """Register a workflow definition"""
        version = workflow.get('version', '1.0.0')
        
        if name not in self.workflows:
            self.workflows[name] = {}
        
        self.workflows[name][version] = workflow
        logger.info(f"Registered workflow: {name} v{version}")
    
    def get_workflow(self, name: str, version: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a workflow definition"""
        if name not in self.workflows:
            return None
        
        if version:
            return self.workflows[name].get(version)
        else:
            # Return latest version
            versions = list(self.workflows[name].keys())
            if not versions:
                return None
            
            # Simple version sorting (assumes semantic versioning)
            latest_version = sorted(versions, reverse=True)[0]
            return self.workflows[name][latest_version]
    
    def list_workflows(self) -> List[str]:
        """List all available workflow names"""
        return list(self.workflows.keys())
    
    def list_workflow_versions(self, name: str) -> List[str]:
        """List all versions of a specific workflow"""
        if name not in self.workflows:
            return []
        return list(self.workflows[name].keys())


class WorkflowLoader:
    """Loads workflows from files and directories"""
    
    def __init__(self):
        self.parser = WorkflowParser()
    
    def load_workflow_file(self, file_path: str) -> Dict[str, Any]:
        """Load workflow from a single file"""
        return self.parser.parse_workflow(file_path)
    
    def load_workflows_directory(self, directory_path: str) -> Dict[str, Dict[str, Any]]:
        """Load all workflows from a directory"""
        workflows = {}
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Workflow directory not found: {directory_path}")
            return workflows
        
        # Find all YAML files
        for workflow_file in directory.glob('*.yaml'):
            try:
                workflow = self.load_workflow_file(str(workflow_file))
                name = workflow.get('name', workflow_file.stem)
                workflows[name] = workflow
                logger.info(f"Loaded workflow: {name} from {workflow_file}")
            except Exception as e:
                logger.error(f"Error loading workflow from {workflow_file}: {e}")
        
        return workflows


def main():
    """Main function for testing the agent coordinator"""
    print("Testing Agent Coordinator...")
    
    # Test workflow parsing
    parser = WorkflowParser()
    print("✓ Workflow parsing components loaded")
    
    # Test agent coordination
    coordinator = AgentCoordinator()
    print("✓ Agent coordinator initialized")
    
    # Test workflow management
    manager = WorkflowManager()
    print("✓ Workflow manager initialized")
    
    # Test workflow loading
    loader = WorkflowLoader()
    print("✓ Workflow loader initialized")
    
    print("Agent Coordinator testing completed!")


if __name__ == "__main__":
    main()