"""
Agent definitions for the AI Project Planner.
This module creates and configures AI agents for project planning tasks.
"""

import yaml
from crewai import Agent
from pathlib import Path


class ProjectAgents:
    """Factory class for creating project planning agents"""
    
    def __init__(self, config_path: str = "config/agents.yaml"):
        """
        Initialize agents factory with configuration
        
        Args:
            config_path: Path to agents configuration YAML file
        """
        self.config_path = Path(config_path)
        self.agents_config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load agents configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                print(f"✅ Agents config loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            print(f"❌ Error: Config file not found at {self.config_path}")
            raise
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML file: {e}")
            raise
    
    def create_project_planning_agent(self) -> Agent:
        """
        Create the Project Planning Agent
        
        Returns:
            Agent configured for project planning tasks
        """
        return Agent(
            config=self.agents_config['project_planning_agent']
        )
    
    def create_estimation_agent(self) -> Agent:
        """
        Create the Estimation Agent
        
        Returns:
            Agent configured for time and resource estimation
        """
        return Agent(
            config=self.agents_config['estimation_agent']
        )
    
    def create_resource_allocation_agent(self) -> Agent:
        """
        Create the Resource Allocation Agent
        
        Returns:
            Agent configured for resource allocation and milestone planning
        """
        return Agent(
            config=self.agents_config['resource_allocation_agent']
        )
    
    def get_all_agents(self) -> list[Agent]:
        """
        Create and return all agents
        
        Returns:
            List of all configured agents
        """
        return [
            self.create_project_planning_agent(),
            self.create_estimation_agent(),
            self.create_resource_allocation_agent()
        ]


# Convenience function for quick agent creation
def create_agents(config_path: str = "config/agents.yaml") -> list[Agent]:
    """
    Quick function to create all agents
    
    Args:
        config_path: Path to agents configuration file
        
    Returns:
        List of all configured agents
    """
    factory = ProjectAgents(config_path)
    return factory.get_all_agents()