#!/usr/bin/env python3
"""
Sub-Agent Configuration Parser and Validator
Parses and validates YAML configuration files for sub-agents
"""

import yaml
import os
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentConfigError(Exception):
    """Custom exception for agent configuration errors"""
    pass

class AgentConfigParser:
    """Parser and validator for sub-agent configurations"""
    
    REQUIRED_FIELDS = [
        'name', 'version', 'description', 'specialization',
        'triggers', 'tools', 'permissions', 'security',
        'behavior', 'integration', 'coordination', 'metadata'
    ]
    
    VALID_PRIORITIES = ['low', 'normal', 'high']
    VALID_VERBOSITY = ['minimal', 'normal', 'detailed']
    VALID_STATUS = ['active', 'inactive', 'deprecated']
    
    def __init__(self, config_dir: str = None):
        """Initialize the parser with configuration directory"""
        if config_dir is None:
            config_dir = os.path.join('.agent-os', 'sub-agents', 'configurations')
        
        self.config_dir = Path(config_dir)
        self.agents = {}
        
    def load_agent_config(self, config_file: str) -> Dict[str, Any]:
        """Load and parse a single agent configuration file"""
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            raise AgentConfigError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise AgentConfigError(f"Invalid YAML in {config_file}: {e}")
        
        # Validate the configuration
        self.validate_config(config, config_file)
        
        return config
    
    def validate_config(self, config: Dict[str, Any], filename: str) -> None:
        """Validate agent configuration structure and values"""
        
        # Check required top-level fields
        for field in self.REQUIRED_FIELDS:
            if field not in config:
                raise AgentConfigError(f"Missing required field '{field}' in {filename}")
        
        # Validate name format
        name = config['name']
        if not isinstance(name, str) or not name.strip():
            raise AgentConfigError(f"Agent name must be a non-empty string in {filename}")
        
        # Validate version format
        version = config['version']
        if not isinstance(version, str) or not version.strip():
            raise AgentConfigError(f"Version must be a non-empty string in {filename}")
        
        # Validate triggers
        self._validate_triggers(config['triggers'], filename)
        
        # Validate tools
        self._validate_tools(config['tools'], filename)
        
        # Validate permissions
        self._validate_permissions(config['permissions'], filename)
        
        # Validate security settings
        self._validate_security(config['security'], filename)
        
        # Validate behavior settings
        self._validate_behavior(config['behavior'], filename)
        
        # Validate coordination settings
        self._validate_coordination(config['coordination'], filename)
        
        # Validate metadata
        self._validate_metadata(config['metadata'], filename)
        
    def _validate_triggers(self, triggers: Dict[str, Any], filename: str) -> None:
        """Validate trigger configuration"""
        if not isinstance(triggers, dict):
            raise AgentConfigError(f"Triggers must be a dictionary in {filename}")
        
        # Validate file_changes if present
        if 'file_changes' in triggers:
            file_changes = triggers['file_changes']
            if not isinstance(file_changes, list):
                raise AgentConfigError(f"file_changes must be a list in {filename}")
            
            for pattern in file_changes:
                if not isinstance(pattern, str):
                    raise AgentConfigError(f"File patterns must be strings in {filename}")
    
    def _validate_tools(self, tools: Dict[str, Any], filename: str) -> None:
        """Validate tools configuration"""
        if not isinstance(tools, dict):
            raise AgentConfigError(f"Tools must be a dictionary in {filename}")
        
        required_tool_fields = ['allowed', 'restricted']
        for field in required_tool_fields:
            if field not in tools:
                raise AgentConfigError(f"Missing tools.{field} in {filename}")
            
            if not isinstance(tools[field], list):
                raise AgentConfigError(f"tools.{field} must be a list in {filename}")
    
    def _validate_permissions(self, permissions: Dict[str, Any], filename: str) -> None:
        """Validate permissions configuration"""
        if not isinstance(permissions, dict):
            raise AgentConfigError(f"Permissions must be a dictionary in {filename}")
        
        required_perm_fields = ['read', 'write', 'execute']
        for field in required_perm_fields:
            if field not in permissions:
                raise AgentConfigError(f"Missing permissions.{field} in {filename}")
            
            if not isinstance(permissions[field], list):
                raise AgentConfigError(f"permissions.{field} must be a list in {filename}")
    
    def _validate_security(self, security: Dict[str, Any], filename: str) -> None:
        """Validate security configuration"""
        if not isinstance(security, dict):
            raise AgentConfigError(f"Security must be a dictionary in {filename}")
        
        # Validate max_file_size
        if 'max_file_size' in security:
            if not isinstance(security['max_file_size'], (int, float)) or security['max_file_size'] <= 0:
                raise AgentConfigError(f"max_file_size must be a positive number in {filename}")
        
        # Validate timeout
        if 'timeout' in security:
            if not isinstance(security['timeout'], int) or security['timeout'] <= 0:
                raise AgentConfigError(f"timeout must be a positive integer in {filename}")
        
        # Validate boolean flags
        bool_fields = ['sandbox_mode', 'audit_logging']
        for field in bool_fields:
            if field in security and not isinstance(security[field], bool):
                raise AgentConfigError(f"security.{field} must be boolean in {filename}")
    
    def _validate_behavior(self, behavior: Dict[str, Any], filename: str) -> None:
        """Validate behavior configuration"""
        if not isinstance(behavior, dict):
            raise AgentConfigError(f"Behavior must be a dictionary in {filename}")
        
        # Validate verbosity
        if 'verbosity' in behavior:
            if behavior['verbosity'] not in self.VALID_VERBOSITY:
                raise AgentConfigError(f"Invalid verbosity '{behavior['verbosity']}' in {filename}")
        
        # Validate max_operations
        if 'max_operations' in behavior:
            if not isinstance(behavior['max_operations'], int) or behavior['max_operations'] <= 0:
                raise AgentConfigError(f"max_operations must be a positive integer in {filename}")
    
    def _validate_coordination(self, coordination: Dict[str, Any], filename: str) -> None:
        """Validate coordination configuration"""
        if not isinstance(coordination, dict):
            raise AgentConfigError(f"Coordination must be a dictionary in {filename}")
        
        # Validate priority
        if 'priority' in coordination:
            if coordination['priority'] not in self.VALID_PRIORITIES:
                raise AgentConfigError(f"Invalid priority '{coordination['priority']}' in {filename}")
        
        # Validate agent lists
        list_fields = ['compatible_agents', 'dependencies']
        for field in list_fields:
            if field in coordination and not isinstance(coordination[field], list):
                raise AgentConfigError(f"coordination.{field} must be a list in {filename}")
    
    def _validate_metadata(self, metadata: Dict[str, Any], filename: str) -> None:
        """Validate metadata configuration"""
        if not isinstance(metadata, dict):
            raise AgentConfigError(f"Metadata must be a dictionary in {filename}")
        
        # Validate status
        if 'status' in metadata:
            if metadata['status'] not in self.VALID_STATUS:
                raise AgentConfigError(f"Invalid status '{metadata['status']}' in {filename}")
    
    def load_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """Load all agent configurations from the directory"""
        if not self.config_dir.exists():
            logger.warning(f"Configuration directory does not exist: {self.config_dir}")
            return {}
        
        agents = {}
        
        for config_file in self.config_dir.glob('*.yaml'):
            # Skip template files
            if config_file.name.startswith('agent-template'):
                continue
                
            try:
                config = self.load_agent_config(config_file.name)
                agent_name = config['name']
                agents[agent_name] = config
                logger.info(f"Loaded agent configuration: {agent_name}")
                
            except AgentConfigError as e:
                logger.error(f"Failed to load {config_file.name}: {e}")
                continue
        
        self.agents = agents
        return agents
    
    def get_agent_config(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific agent"""
        return self.agents.get(agent_name)
    
    def list_active_agents(self) -> List[str]:
        """Get list of active agent names"""
        active_agents = []
        for name, config in self.agents.items():
            if config.get('metadata', {}).get('status') == 'active':
                active_agents.append(name)
        return active_agents
    
    def validate_agent_compatibility(self, agent1: str, agent2: str) -> bool:
        """Check if two agents are compatible for coordination"""
        config1 = self.get_agent_config(agent1)
        config2 = self.get_agent_config(agent2)
        
        if not config1 or not config2:
            return False
        
        # Check if agent1 lists agent2 as compatible
        compatible1 = config1.get('coordination', {}).get('compatible_agents', [])
        if agent2 in compatible1:
            return True
        
        # Check if agent2 lists agent1 as compatible
        compatible2 = config2.get('coordination', {}).get('compatible_agents', [])
        if agent1 in compatible2:
            return True
        
        return False


def main():
    """Command-line interface for the agent config parser"""
    parser = AgentConfigParser()
    
    try:
        agents = parser.load_all_agents()
        
        if not agents:
            print("No agent configurations found.")
            return
        
        print(f"Successfully loaded {len(agents)} agent configurations:")
        for name, config in agents.items():
            status = config.get('metadata', {}).get('status', 'unknown')
            print(f"  - {name}: {config['description']} (status: {status})")
        
        # List active agents
        active_agents = parser.list_active_agents()
        print(f"\nActive agents: {', '.join(active_agents)}")
        
    except Exception as e:
        logger.error(f"Error loading agent configurations: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()