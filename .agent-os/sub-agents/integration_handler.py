#!/usr/bin/env python3
"""
Integration Handler - Interface between sub-agents and Claude Code/Agent OS
Provides commands, result formatting, and monitoring for sub-agent system
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClaudeCodeIntegration:
    """Integration with Claude Code interface"""
    
    def __init__(self):
        self.registered_commands = {}
        self.agent_coordinator = None
        self.config_parser = None
        self._setup_integration()
    
    def _setup_integration(self):
        """Set up integration components"""
        try:
            # Import sub-agent components
            from agent_coordinator import AgentCoordinator
            from agent_config_parser import AgentConfigParser
            
            # Initialize components
            config_dir = Path(__file__).parent / "configurations"
            self.config_parser = AgentConfigParser(str(config_dir))
            
            # Load all agents into the parser's agents dictionary
            self.config_parser.agents = self.config_parser.load_all_agents()
            
            self.agent_coordinator = AgentCoordinator(self.config_parser)
            
            # Register commands
            self._register_commands()
            
        except ImportError as e:
            logger.error(f"Failed to import sub-agent components: {e}")
        except Exception as e:
            logger.error(f"Failed to setup integration: {e}")
    
    def _register_commands(self):
        """Register sub-agent commands with Claude Code"""
        self.registered_commands = {
            'run-agent': {
                'description': 'Execute a single sub-agent',
                'parameters': {
                    'agent': 'Agent name (required)',
                    'action': 'Action to perform (optional)',
                    'target': 'Target files or pattern (optional)',
                    'context': 'Additional context (optional)'
                },
                'examples': [
                    'run-agent code-quality-agent analyze *.py',
                    'run-agent documentation-agent update'
                ]
            },
            'run-workflow': {
                'description': 'Execute a predefined workflow',
                'parameters': {
                    'workflow': 'Workflow name (required)',
                    'context': 'Workflow context (optional)',
                    'parallel': 'Enable parallel execution (optional)'
                },
                'examples': [
                    'run-workflow code-quality-check',
                    'run-workflow resume-processing'
                ]
            },
            'list-agents': {
                'description': 'List all available sub-agents',
                'parameters': {},
                'examples': ['list-agents']
            },
            'agent-status': {
                'description': 'Get status of specific agent',
                'parameters': {
                    'agent': 'Agent name (required)'
                },
                'examples': ['agent-status code-quality-agent']
            },
            'list-workflows': {
                'description': 'List available workflows',
                'parameters': {},
                'examples': ['list-workflows']
            },
            'workflow-status': {
                'description': 'Get status of workflow execution',
                'parameters': {
                    'workflow_id': 'Workflow execution ID (required)'
                },
                'examples': ['workflow-status workflow_12345']
            }
        }
    
    def get_registered_commands(self) -> Dict[str, Any]:
        """Get all registered commands"""
        return self.registered_commands
    
    def execute_command(self, command: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a sub-agent command"""
        try:
            if command == 'run-agent':
                return self._execute_agent_command(parameters)
            elif command == 'run-workflow':
                return self._execute_workflow_command(parameters)
            elif command == 'list-agents':
                return self._list_agents_command()
            elif command == 'agent-status':
                return self._agent_status_command(parameters)
            elif command == 'list-workflows':
                return self._list_workflows_command()
            elif command == 'workflow-status':
                return self._workflow_status_command(parameters)
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown command: {command}',
                    'available_commands': list(self.registered_commands.keys())
                }
        except Exception as e:
            logger.error(f"Error executing command {command}: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'command': command,
                'parameters': parameters
            }
    
    def _execute_agent_command(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute single agent command"""
        agent_name = parameters.get('agent')
        if not agent_name:
            return {'status': 'error', 'error': 'Agent name is required'}
        
        action = parameters.get('action', 'default')
        target = parameters.get('target', '')
        context = parameters.get('context', {})
        
        # Prepare agent parameters
        agent_params = {
            'target': target,
            'context': context
        }
        
        # Execute agent through coordinator
        start_time = datetime.now()
        try:
            result = self.agent_coordinator._execute_agent(agent_name, action, agent_params)
            result['agent'] = agent_name
            result['command'] = 'run-agent'
            result['execution_time'] = (datetime.now() - start_time).total_seconds()
            return result
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'agent': agent_name,
                'action': action,
                'execution_time': (datetime.now() - start_time).total_seconds()
            }
    
    def _execute_workflow_command(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow command"""
        workflow_name = parameters.get('workflow')
        if not workflow_name:
            return {'status': 'error', 'error': 'Workflow name is required'}
        
        context = parameters.get('context', {})
        
        # Load predefined workflow
        workflow_def = self._get_predefined_workflow(workflow_name)
        if not workflow_def:
            return {
                'status': 'error',
                'error': f'Unknown workflow: {workflow_name}',
                'available_workflows': self._get_available_workflow_names()
            }
        
        # Add context to workflow
        if context:
            workflow_def['context'] = {**workflow_def.get('context', {}), **context}
        
        # Execute workflow
        try:
            result = self.agent_coordinator.execute_workflow(workflow_def)
            result['command'] = 'run-workflow'
            return result
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'workflow': workflow_name,
                'context': context
            }
    
    def _list_agents_command(self) -> Dict[str, Any]:
        """List available agents command"""
        try:
            agents = self.agent_coordinator.discover_agents()
            return {
                'status': 'success',
                'command': 'list-agents',
                'count': len(agents),
                'agents': agents
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'command': 'list-agents'
            }
    
    def _agent_status_command(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get agent status command"""
        agent_name = parameters.get('agent')
        if not agent_name:
            return {'status': 'error', 'error': 'Agent name is required'}
        
        try:
            # Get agent configuration
            if self.config_parser:
                config = self.config_parser.get_agent_config(agent_name)
                if config:
                    return {
                        'status': 'success',
                        'command': 'agent-status',
                        'agent': agent_name,
                        'agent_status': config.get('metadata', {}).get('status', 'unknown'),
                        'specialization': config.get('specialization', 'unknown'),
                        'version': config.get('version', '1.0.0'),
                        'last_execution': 'N/A',  # Would track in real implementation
                        'capabilities': config.get('metadata', {}).get('capabilities', [])
                    }
                else:
                    return {
                        'status': 'error',
                        'agent': agent_name,
                        'error': f'Agent not found: {agent_name}',
                        'available_agents': [a['name'] for a in self.agent_coordinator.discover_agents()]
                    }
            else:
                return {'status': 'error', 'error': 'Configuration parser not available'}
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'agent': agent_name
            }
    
    def _list_workflows_command(self) -> Dict[str, Any]:
        """List available workflows command"""
        try:
            workflows = self._get_available_workflows()
            return {
                'status': 'success',
                'command': 'list-workflows',
                'count': len(workflows),
                'workflows': workflows
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'command': 'list-workflows'
            }
    
    def _workflow_status_command(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Get workflow status command"""
        workflow_id = parameters.get('workflow_id')
        if not workflow_id:
            return {'status': 'error', 'error': 'Workflow ID is required'}
        
        # In real implementation, would track workflow executions
        return {
            'status': 'success',
            'command': 'workflow-status',
            'workflow_id': workflow_id,
            'execution_status': 'not_implemented',
            'message': 'Workflow status tracking not yet implemented'
        }
    
    def _get_predefined_workflow(self, workflow_name: str) -> Optional[Dict[str, Any]]:
        """Get predefined workflow definition"""
        # Predefined workflows for common tasks
        workflows = {
            'code-quality-check': {
                'name': 'code-quality-check',
                'execution': {'type': 'sequential'},
                'steps': [
                    {
                        'agent': 'code-quality-agent',
                        'action': 'analyze_codebase',
                        'output_key': 'quality_results'
                    },
                    {
                        'agent': 'documentation-agent',
                        'action': 'validate_documentation',
                        'depends_on': 'code-quality-agent',
                        'condition': 'quality_results.issues_found > 0'
                    }
                ]
            },
            'resume-processing': {
                'name': 'resume-processing',
                'execution': {'type': 'sequential'},
                'steps': [
                    {
                        'agent': 'resume-processing-agent',
                        'action': 'validate_resume',
                        'output_key': 'resume_validation'
                    },
                    {
                        'agent': 'content-generation-agent',
                        'action': 'generate_content_suite',
                        'depends_on': 'resume-processing-agent',
                        'condition': 'resume_validation.quality_score > 70',
                        'input_from': 'resume_validation'
                    }
                ]
            },
            'maintenance-check': {
                'name': 'maintenance-check',
                'execution': {'type': 'parallel', 'max_concurrent': 2},
                'steps': [
                    {
                        'group': 'maintenance_group',
                        'parallel': True,
                        'agents': [
                            {
                                'agent': 'maintenance-agent',
                                'action': 'dependency_health_check'
                            },
                            {
                                'agent': 'maintenance-agent',
                                'action': 'security_vulnerability_scan'
                            }
                        ]
                    }
                ]
            }
        }
        return workflows.get(workflow_name)
    
    def _get_available_workflows(self) -> List[Dict[str, Any]]:
        """Get list of available workflows"""
        workflow_definitions = {
            'code-quality-check': 'Comprehensive code quality analysis',
            'resume-processing': 'Resume validation and content generation',
            'maintenance-check': 'Project maintenance and security scanning'
        }
        
        workflows = []
        for name, description in workflow_definitions.items():
            workflows.append({
                'name': name,
                'description': description,
                'type': 'predefined'
            })
        
        return workflows
    
    def _get_available_workflow_names(self) -> List[str]:
        """Get list of available workflow names"""
        return [w['name'] for w in self._get_available_workflows()]


class AgentOSIntegration:
    """Integration with Agent OS framework"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.agent_os_dir = self.project_root / ".agent-os"
        self.specs_dir = self.agent_os_dir / "specs"
        self.product_dir = self.agent_os_dir / "product"
    
    def discover_workflows(self) -> List[Dict[str, Any]]:
        """Discover workflows from Agent OS specs and configurations"""
        workflows = []
        
        # Add predefined workflows
        predefined = [
            {
                'name': 'code-quality-check',
                'description': 'Comprehensive code quality analysis',
                'type': 'predefined',
                'agents': ['code-quality-agent', 'documentation-agent']
            },
            {
                'name': 'resume-processing',
                'description': 'Resume validation and content generation',
                'type': 'predefined',
                'agents': ['resume-processing-agent', 'content-generation-agent']
            },
            {
                'name': 'maintenance-check',
                'description': 'Project maintenance and security scanning',
                'type': 'predefined',
                'agents': ['maintenance-agent']
            }
        ]
        workflows.extend(predefined)
        
        # Discover spec-based workflows
        if self.specs_dir.exists():
            for spec_dir in self.specs_dir.iterdir():
                if spec_dir.is_dir():
                    tasks_file = spec_dir / "tasks.md"
                    if tasks_file.exists():
                        workflows.append({
                            'name': f'spec-{spec_dir.name}',
                            'description': f'Execute tasks from spec {spec_dir.name}',
                            'type': 'spec-based',
                            'spec_path': str(spec_dir),
                            'agents': ['code-quality-agent', 'documentation-agent']  # Default agents
                        })
        
        return workflows
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate Agent OS configuration for sub-agents"""
        validation_result = {
            'valid': True,
            'agents_configured': 0,
            'workflows_available': 0,
            'issues': []
        }
        
        try:
            # Check if .agent-os directory exists
            if not self.agent_os_dir.exists():
                validation_result['issues'].append("Agent OS directory not found")
                validation_result['valid'] = False
                return validation_result
            
            # Check sub-agents directory
            sub_agents_dir = self.agent_os_dir / "sub-agents"
            if not sub_agents_dir.exists():
                validation_result['issues'].append("Sub-agents directory not found")
                validation_result['valid'] = False
            else:
                # Count configured agents
                config_dir = sub_agents_dir / "configurations"
                if config_dir.exists():
                    yaml_files = list(config_dir.glob("*.yaml"))
                    validation_result['agents_configured'] = len([f for f in yaml_files if not f.name.startswith('agent-template')])
            
            # Count available workflows
            workflows = self.discover_workflows()
            validation_result['workflows_available'] = len(workflows)
            
            # Check CLAUDE.md integration
            claude_md = self.project_root / "CLAUDE.md"
            if claude_md.exists():
                content = claude_md.read_text(encoding='utf-8')
                if 'sub-agents' not in content.lower():
                    validation_result['issues'].append("CLAUDE.md doesn't mention sub-agents integration")
            else:
                validation_result['issues'].append("CLAUDE.md not found")
            
        except Exception as e:
            validation_result['valid'] = False
            validation_result['issues'].append(f"Validation error: {str(e)}")
        
        return validation_result
    
    def execute_spec_with_agents(self, spec_path: str, agents: List[str]) -> Dict[str, Any]:
        """Execute spec tasks using sub-agents"""
        result = {
            'spec_status': 'not_implemented',
            'agent_contributions': {},
            'message': 'Spec execution with agents not yet fully implemented'
        }
        
        # This would integrate with Agent OS spec execution
        # For now, return mock result
        for agent in agents:
            result['agent_contributions'][agent] = {
                'tasks_completed': 0,
                'contribution': 'Mock contribution - not yet implemented'
            }
        
        return result
    
    def parse_claude_md_instructions(self) -> Dict[str, Any]:
        """Parse CLAUDE.md for sub-agent instructions"""
        instructions = {
            'sub_agent_workflows': [],
            'agent_coordination_rules': [],
            'integration_settings': {}
        }
        
        try:
            claude_md = self.project_root / "CLAUDE.md"
            if claude_md.exists():
                content = claude_md.read_text(encoding='utf-8')
                
                # Look for sub-agent related sections
                if 'sub-agents' in content.lower():
                    instructions['integration_settings']['sub_agents_enabled'] = True
                
                # Parse workflow references
                workflow_pattern = r'workflow[:\s]+([a-zA-Z0-9-_]+)'
                workflows = re.findall(workflow_pattern, content, re.IGNORECASE)
                instructions['sub_agent_workflows'] = list(set(workflows))
                
        except Exception as e:
            logger.error(f"Error parsing CLAUDE.md: {e}")
            instructions['error'] = str(e)
        
        return instructions


class ResultFormatter:
    """Formats agent and workflow results for display"""
    
    def __init__(self):
        self.timestamp_format = "%Y-%m-%d %H:%M:%S"
    
    def format_agent_result(self, result: Dict[str, Any]) -> str:
        """Format single agent execution result"""
        agent = result.get('agent', 'unknown')
        status = result.get('status', 'unknown')
        duration = result.get('duration', result.get('execution_time', 0))
        
        # Format header
        header = f"🤖 Agent: {agent}"
        status_line = f"Status: {'✅ ' + status.upper() if status == 'success' else '❌ ' + status.upper()}"
        timing_line = f"Duration: {duration:.1f}s"
        
        formatted = f"{header}\n{status_line}\n{timing_line}\n"
        
        # Format results
        if status == 'success' and 'results' in result:
            results = result['results']
            formatted += "\nResults:\n"
            
            for key, value in results.items():
                if isinstance(value, (int, float)):
                    formatted += f"  • {key}: {value}\n"
                elif isinstance(value, bool):
                    formatted += f"  • {key}: {'Yes' if value else 'No'}\n"
                elif isinstance(value, list):
                    formatted += f"  • {key}: {len(value)} items\n"
                else:
                    formatted += f"  • {key}: {value}\n"
        
        # Format errors
        if status == 'error' and 'error' in result:
            formatted += f"\n❌ Error: {result['error']}\n"
        
        return formatted
    
    def format_workflow_result(self, result: Dict[str, Any]) -> str:
        """Format workflow execution result"""
        workflow_name = result.get('workflow_name', 'unknown')
        status = result.get('status', 'unknown')
        duration = result.get('duration_seconds', 0)
        agent_results = result.get('agent_results', [])
        errors = result.get('errors', [])
        
        # Format header
        header = f"🔄 Workflow: {workflow_name}"
        status_line = f"Status: {'✅ ' + status if status == 'completed' else '❌ ' + status.upper()}"
        timing_line = f"Duration: {duration:.1f}s"
        agents_line = f"{len(agent_results)} agents executed"
        
        formatted = f"{header}\n{status_line}\n{timing_line}\n{agents_line}\n"
        
        # Format agent summaries
        if agent_results:
            formatted += "\nAgent Results:\n"
            for agent_result in agent_results:
                agent = agent_result.get('agent', 'unknown')
                agent_status = agent_result.get('status', 'unknown')
                agent_duration = agent_result.get('duration', 0)
                
                status_icon = '✅' if agent_status == 'success' else '❌'
                formatted += f"  {status_icon} {agent}: {agent_status} ({agent_duration:.1f}s)\n"
        
        # Format errors
        if errors:
            formatted += f"\n⚠️ Errors ({len(errors)}):\n"
            for error in errors[:3]:  # Show first 3 errors
                error_msg = error.get('message', str(error))
                formatted += f"  • {error_msg}\n"
            if len(errors) > 3:
                formatted += f"  • ... and {len(errors) - 3} more errors\n"
        
        return formatted
    
    def format_error_result(self, result: Dict[str, Any]) -> str:
        """Format error result"""
        agent = result.get('agent', 'unknown')
        error = result.get('error', 'Unknown error')
        timestamp = result.get('timestamp', datetime.now().isoformat())
        
        formatted = f"❌ ERROR in {agent}\n"
        formatted += f"Message: {error}\n"
        formatted += f"Time: {timestamp}\n"
        
        return formatted
    
    def format_agent_list(self, agents: List[Dict[str, Any]]) -> str:
        """Format list of available agents"""
        if not agents:
            return "No agents available"
        
        formatted = f"📋 Available Agents ({len(agents)}):\n\n"
        
        for agent in agents:
            name = agent.get('name', 'unknown')
            specialization = agent.get('specialization', 'unknown')
            status = agent.get('status', 'unknown')
            version = agent.get('version', '1.0.0')
            
            status_icon = '🟢' if status == 'active' else '🔴'
            formatted += f"{status_icon} {name} (v{version})\n"
            formatted += f"   Specialization: {specialization}\n"
            
            capabilities = agent.get('capabilities', [])
            if capabilities:
                formatted += f"   Capabilities: {len(capabilities)} available\n"
            formatted += "\n"
        
        return formatted
    
    def format_workflow_list(self, workflows: List[Dict[str, Any]]) -> str:
        """Format list of available workflows"""
        if not workflows:
            return "No workflows available"
        
        formatted = f"📋 Available Workflows ({len(workflows)}):\n\n"
        
        for workflow in workflows:
            name = workflow.get('name', 'unknown')
            description = workflow.get('description', 'No description')
            workflow_type = workflow.get('type', 'unknown')
            agents = workflow.get('agents', [])
            
            type_icon = '⚡' if workflow_type == 'predefined' else '📝'
            formatted += f"{type_icon} {name}\n"
            formatted += f"   Description: {description}\n"
            formatted += f"   Type: {workflow_type}\n"
            
            if agents:
                formatted += f"   Agents: {', '.join(agents)}\n"
            formatted += "\n"
        
        return formatted


class ProgressDisplay:
    """Real-time progress display for workflow execution"""
    
    def __init__(self):
        self.current_workflow = None
        self.agent_progress = {}
        self.start_time = None
        self.total_agents = 0
    
    def start_workflow(self, workflow_name: str, total_agents: int):
        """Start workflow progress tracking"""
        self.current_workflow = workflow_name
        self.total_agents = total_agents
        self.agent_progress = {}
        self.start_time = datetime.now()
    
    def update_agent_progress(self, agent: str, status: str, progress: int):
        """Update individual agent progress"""
        self.agent_progress[agent] = {
            'status': status,
            'progress': progress,
            'updated': datetime.now()
        }
    
    def get_current_display(self) -> str:
        """Get current progress display"""
        if not self.current_workflow:
            return "No active workflow"
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        # Header
        display = f"🔄 Workflow: {self.current_workflow}\n"
        display += f"⏱️ Elapsed: {elapsed:.1f}s\n"
        display += f"👥 Agents: {len(self.agent_progress)}/{self.total_agents}\n\n"
        
        # Agent progress
        for agent, info in self.agent_progress.items():
            status = info['status']
            progress = info['progress']
            
            status_icon = {
                'pending': '⏳',
                'running': '🔄',
                'completed': '✅',
                'error': '❌'
            }.get(status, '❓')
            
            # Progress bar
            bar_length = 20
            filled = int(bar_length * progress / 100)
            bar = '█' * filled + '░' * (bar_length - filled)
            
            display += f"{status_icon} {agent}: [{bar}] {progress}% ({status})\n"
        
        return display
    
    def get_completion_summary(self) -> str:
        """Get workflow completion summary"""
        if not self.current_workflow:
            return "No workflow completed"
        
        total_time = (datetime.now() - self.start_time).total_seconds()
        completed = len([a for a in self.agent_progress.values() if a['status'] == 'completed'])
        errors = len([a for a in self.agent_progress.values() if a['status'] == 'error'])
        
        summary = f"✅ Workflow Complete: {self.current_workflow}\n"
        summary += f"⏱️ Total Time: {total_time:.1f}s\n"
        summary += f"✅ Completed: {completed}/{self.total_agents}\n"
        if errors > 0:
            summary += f"❌ Errors: {errors}\n"
        
        return summary


class CommandParser:
    """Parses user commands for sub-agent operations"""
    
    def __init__(self):
        self.command_patterns = {
            'run_agent': [
                r'run agent (\w+)',
                r'execute agent (\w+)',
                r'(\w+) agent'
            ],
            'run_workflow': [
                r'run workflow (\w+)',
                r'execute workflow (\w+)',
                r'workflow (\w+)'
            ],
            'list_agents': [
                r'list agents',
                r'show agents',
                r'agents'
            ],
            'list_workflows': [
                r'list workflows',
                r'show workflows',
                r'workflows'
            ]
        }
    
    def parse_command(self, command_text: str) -> Dict[str, Any]:
        """Parse command text into structured command"""
        command_text = command_text.lower().strip()
        
        for action, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_text)
                if match:
                    return self._extract_command_details(action, command_text, match)
        
        # Default fallback
        return {
            'action': 'unknown',
            'parameters': {},
            'original_text': command_text,
            'error': 'Could not parse command'
        }
    
    def _extract_command_details(self, action: str, command_text: str, match) -> Dict[str, Any]:
        """Extract detailed command parameters"""
        result = {
            'action': action,
            'parameters': {},
            'original_text': command_text
        }
        
        if action == 'run_agent':
            result['parameters']['agent'] = match.group(1)
            
            # Extract additional parameters
            if ' on ' in command_text:
                target = command_text.split(' on ')[1].strip()
                result['parameters']['target'] = target
            
            if ' with ' in command_text:
                context_part = command_text.split(' with ')[1].strip()
                result['parameters']['context'] = self._parse_context(context_part)
        
        elif action == 'run_workflow':
            result['parameters']['workflow'] = match.group(1)
            
            # Extract context
            if ' with ' in command_text:
                context_part = command_text.split(' with ')[1].strip()
                result['parameters']['context'] = self._parse_context(context_part)
        
        return result
    
    def _parse_context(self, context_text: str) -> Dict[str, Any]:
        """Parse context parameters from text"""
        context = {}
        
        # Simple key=value parsing
        pairs = context_text.split(',')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                context[key.strip()] = value.strip()
        
        return context


class CommandValidator:
    """Validates user commands before execution"""
    
    def __init__(self):
        self.required_parameters = {
            'run_agent': ['agent'],
            'run_workflow': ['workflow'],
            'agent_status': ['agent'],
            'workflow_status': ['workflow_id']
        }
    
    def validate_command(self, command: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate command structure and parameters"""
        errors = []
        
        # Check action
        action = command.get('action')
        if not action:
            errors.append("Missing command action")
            return False, errors
        
        # Check required parameters
        if action in self.required_parameters:
            required = self.required_parameters[action]
            parameters = command.get('parameters', {})
            
            for param in required:
                if param not in parameters or not parameters[param]:
                    errors.append(f"Missing required parameter: {param}")
        
        return len(errors) == 0, errors


class HelpGenerator:
    """Generates help text for sub-agent commands"""
    
    def __init__(self):
        self.claude_integration = ClaudeCodeIntegration()
    
    def generate_general_help(self) -> str:
        """Generate general help for sub-agent system"""
        help_text = """
🤖 Sub-Agent System Help

The sub-agent system provides specialized AI agents for different tasks:

Available Commands:
• run-agent <agent-name> [action] [target] - Execute a single agent
• run-workflow <workflow-name> [context] - Execute a predefined workflow
• list-agents - Show all available agents
• list-workflows - Show all available workflows
• agent-status <agent-name> - Get status of specific agent

Examples:
• run-agent code-quality-agent analyze *.py
• run-workflow code-quality-check
• list-agents
• agent-status maintenance-agent

Available Agents:
• code-quality-agent - Code analysis and quality metrics
• documentation-agent - Documentation maintenance and validation
• resume-processing-agent - Resume validation and PDF generation
• content-generation-agent - LinkedIn posts and professional content
• maintenance-agent - Dependency monitoring and security scanning

Available Workflows:
• code-quality-check - Comprehensive code quality analysis
• resume-processing - Resume validation and content generation
• maintenance-check - Project maintenance and security scanning

For detailed help on specific agents or workflows, use:
• agent-help <agent-name>
• workflow-help <workflow-name>
"""
        return help_text.strip()
    
    def generate_agent_help(self, agent_name: str) -> str:
        """Generate help for specific agent"""
        agent_help = {
            'code-quality-agent': """
🔍 Code Quality Agent Help

Specialization: Code analysis and quality metrics
Actions: analyze, analyze_codebase, quality_report

Usage:
• run-agent code-quality-agent analyze *.py
• run-agent code-quality-agent analyze_codebase

Capabilities:
• Python code analysis
• Code complexity assessment
• Style consistency checking
• Quality score calculation
• Improvement recommendations
""",
            'documentation-agent': """
📚 Documentation Agent Help

Specialization: Documentation maintenance and validation
Actions: update, validate_documentation, check_links

Usage:
• run-agent documentation-agent update
• run-agent documentation-agent validate_documentation

Capabilities:
• Cross-reference validation
• Link checking
• Documentation completeness assessment
• README maintenance
• Project structure validation
""",
            'maintenance-agent': """
🔧 Maintenance Agent Help

Specialization: Project maintenance and monitoring
Actions: check_dependencies, security_scan, health_check

Usage:
• run-agent maintenance-agent check_dependencies
• run-agent maintenance-agent security_scan

Capabilities:
• Dependency monitoring
• Security vulnerability scanning
• Project health metrics
• Outdated package detection
• Maintenance recommendations
"""
        }
        
        return agent_help.get(agent_name, f"No help available for agent: {agent_name}")
    
    def generate_workflow_help(self, workflow_name: str) -> str:
        """Generate help for specific workflow"""
        workflow_help = {
            'code-quality-check': """
🔄 Code Quality Check Workflow

Description: Comprehensive code quality analysis
Execution: Sequential (code-quality-agent → documentation-agent)

Steps:
1. Code Quality Agent analyzes codebase
2. Documentation Agent validates documentation (if issues found)

Usage:
• run-workflow code-quality-check
• run-workflow code-quality-check with strict_mode=true

Output:
• Quality score and recommendations
• Documentation validation results
• Overall project health assessment
""",
            'resume-processing': """
🔄 Resume Processing Workflow

Description: Resume validation and content generation
Execution: Sequential (resume-processing-agent → content-generation-agent)

Steps:
1. Resume Processing Agent validates resume format
2. Content Generation Agent creates LinkedIn content (if quality > 70%)

Usage:
• run-workflow resume-processing
• run-workflow resume-processing with generate_all=true

Output:
• Resume validation results
• Generated LinkedIn posts
• Professional bio content
"""
        }
        
        return workflow_help.get(workflow_name, f"No help available for workflow: {workflow_name}")


class ExecutionLogger:
    """Logs agent and workflow executions"""
    
    def __init__(self):
        self.execution_history = []
        self.log_file = Path(__file__).parent / "logs" / "execution.log"
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log_agent_execution(self, agent: str, action: str, status: str, 
                          duration: float, results: Dict[str, Any]):
        """Log agent execution"""
        log_entry = {
            'type': 'agent',
            'timestamp': datetime.now().isoformat(),
            'agent': agent,
            'action': action,
            'status': status,
            'duration': duration,
            'results': results
        }
        
        self.execution_history.append(log_entry)
        self._write_log_entry(log_entry)
    
    def log_workflow_execution(self, workflow: str, status: str, duration: float, 
                             agents_executed: List[str]):
        """Log workflow execution"""
        log_entry = {
            'type': 'workflow',
            'timestamp': datetime.now().isoformat(),
            'workflow': workflow,
            'status': status,
            'duration': duration,
            'agents_executed': agents_executed
        }
        
        self.execution_history.append(log_entry)
        self._write_log_entry(log_entry)
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.execution_history.copy()
    
    def _write_log_entry(self, entry: Dict[str, Any]):
        """Write log entry to file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            logger.error(f"Failed to write log entry: {e}")


class PerformanceMonitor:
    """Monitors performance of agent and workflow executions"""
    
    def __init__(self):
        self.monitoring_sessions = {}
        self.performance_data = {}
    
    def start_monitoring_session(self, workflow_name: str) -> str:
        """Start performance monitoring session"""
        session_id = f"session_{int(time.time())}"
        self.monitoring_sessions[session_id] = {
            'workflow_name': workflow_name,
            'start_time': time.time(),
            'agents': {},
            'metrics': {}
        }
        return session_id
    
    def record_agent_metrics(self, session_id: str, agent: str, metrics: Dict[str, Any]):
        """Record agent performance metrics"""
        if session_id in self.monitoring_sessions:
            self.monitoring_sessions[session_id]['agents'][agent] = {
                'metrics': metrics,
                'recorded_at': time.time()
            }
    
    def get_performance_summary(self, session_id: str) -> Dict[str, Any]:
        """Get performance summary for session"""
        if session_id not in self.monitoring_sessions:
            return {'error': 'Session not found'}
        
        session = self.monitoring_sessions[session_id]
        
        total_cpu = sum(agent['metrics'].get('cpu_usage', 0) 
                       for agent in session['agents'].values())
        peak_memory = max((agent['metrics'].get('memory_usage', 0) 
                          for agent in session['agents'].values()), default=0)
        total_execution_time = sum(agent['metrics'].get('execution_time', 0) 
                                  for agent in session['agents'].values())
        
        return {
            'session_id': session_id,
            'workflow_name': session['workflow_name'],
            'total_cpu_usage': total_cpu,
            'peak_memory_usage': peak_memory,
            'total_execution_time': total_execution_time,
            'agents_monitored': len(session['agents'])
        }


class ErrorTracker:
    """Tracks and reports errors in sub-agent system"""
    
    def __init__(self):
        self.error_log = []
        self.error_stats = {}
    
    def record_error(self, component: str, error_type: str, message: str, 
                    context: Dict[str, Any]):
        """Record an error occurrence"""
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'error_type': error_type,
            'message': message,
            'context': context
        }
        
        self.error_log.append(error_entry)
        
        # Update statistics
        if error_type not in self.error_stats:
            self.error_stats[error_type] = 0
        self.error_stats[error_type] += 1
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics"""
        recent_errors = []
        for e in self.error_log:
            try:
                # Try to parse timestamp and check if recent (last 7 days)
                ts_str = e['timestamp']
                if '.' in ts_str:
                    timestamp = datetime.strptime(ts_str, '%Y-%m-%dT%H:%M:%S.%f')
                else:
                    timestamp = datetime.strptime(ts_str, '%Y-%m-%dT%H:%M:%S')
                if (datetime.now() - timestamp).days < 7:
                    recent_errors.append(e)
            except (ValueError, KeyError):
                # Skip entries with invalid timestamps
                continue
        
        return {
            'total_errors': len(self.error_log),
            'recent_errors': len(recent_errors),
            'errors_by_type': self.error_stats.copy(),
            'most_recent': self.error_log[-5:] if self.error_log else []
        }


class ConfigurationManager:
    """Manages agent and workflow configurations"""
    
    def __init__(self):
        self.config_dir = Path(__file__).parent / "configurations"
        self.workflow_dir = Path(__file__).parent / "coordination"
        self.custom_workflows = []  # Track custom workflows
    
    def update_agent_config(self, agent: str, updates: Dict[str, Any]) -> bool:
        """Update agent configuration"""
        config_file = self.config_dir / f"{agent}.yaml"
        
        if not config_file.exists():
            return False
        
        try:
            import yaml
            
            # Load current config
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Apply updates (deep merge)
            self._deep_merge(config, updates)
            
            # Save updated config
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config, f, default_flow_style=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update agent config {agent}: {e}")
            return False
    
    def create_custom_workflow(self, name: str, agents: List[str], 
                             execution_type: str) -> bool:
        """Create custom workflow definition"""
        workflow_def = {
            'name': name,
            'description': f'Custom workflow: {name}',
            'agents': [{'name': agent, 'required': True} for agent in agents],
            'execution': {'type': execution_type},
            'steps': []
        }
        
        # Add basic steps
        for i, agent in enumerate(agents):
            step = {
                'agent': agent,
                'action': 'default'
            }
            if i > 0:
                step['depends_on'] = agents[i-1]
            workflow_def['steps'].append(step)
        
        # Save workflow to custom workflows list
        self.custom_workflows.append({'name': name, 'type': 'custom', 'definition': workflow_def})
        logger.info(f"Created custom workflow: {name}")
        return True
    
    def get_agent_config(self, agent: str) -> Optional[Dict[str, Any]]:
        """Get agent configuration"""
        config_file = self.config_dir / f"{agent}.yaml"
        
        if not config_file.exists():
            return None
        
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load agent config {agent}: {e}")
            return None
    
    def list_available_workflows(self) -> List[Dict[str, Any]]:
        """List available workflows"""
        # Predefined workflows
        workflows = [
            {'name': 'code-quality-check', 'type': 'predefined'},
            {'name': 'resume-processing', 'type': 'predefined'},
            {'name': 'maintenance-check', 'type': 'predefined'}
        ]
        
        # Add custom workflows
        workflows.extend(self.custom_workflows)
        
        return workflows
    
    def update_global_settings(self, settings: Dict[str, Any]) -> bool:
        """Update global sub-agent settings"""
        # Mock implementation
        logger.info(f"Updated global settings: {settings}")
        return True
    
    def get_global_settings(self) -> Dict[str, Any]:
        """Get global sub-agent settings"""
        # Mock implementation
        return {
            'max_concurrent_agents': 5,
            'default_timeout': 600,
            'enable_audit_logging': True
        }
    
    def _deep_merge(self, target: Dict[str, Any], source: Dict[str, Any]):
        """Deep merge source dict into target dict"""
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value


def main():
    """Main function for testing integration components"""
    print("Testing Integration Components...")
    
    # Test Claude Code integration
    claude_integration = ClaudeCodeIntegration()
    commands = claude_integration.get_registered_commands()
    print(f"✓ Registered {len(commands)} commands with Claude Code")
    
    # Test Agent OS integration
    agent_os_integration = AgentOSIntegration()
    workflows = agent_os_integration.discover_workflows()
    print(f"✓ Discovered {len(workflows)} workflows")
    
    # Test result formatting
    formatter = ResultFormatter()
    print("✓ Result formatter initialized")
    
    # Test command parsing
    parser = CommandParser()
    test_command = parser.parse_command("run agent code-quality-agent on *.py")
    print(f"✓ Command parser working: {test_command['action']}")
    
    print("Integration components testing completed!")


if __name__ == "__main__":
    main()