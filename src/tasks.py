"""
Task definitions for the AI Project Planner.
This module creates and configures tasks for AI agents.
"""

import yaml
from crewai import Task, Agent
from pathlib import Path
from typing import Optional


class ProjectTasks:
    """Factory class for creating project planning tasks"""
    
    def __init__(self, config_path: str = "config/tasks.yaml"):
        """
        Initialize tasks factory with configuration
        
        Args:
            config_path: Path to tasks configuration YAML file
        """
        self.config_path = Path(config_path)
        self.tasks_config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load tasks configuration from YAML file"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
                print(f"✅ Tasks config loaded from {self.config_path}")
                return config
        except FileNotFoundError:
            print(f"❌ Error: Config file not found at {self.config_path}")
            raise
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML file: {e}")
            raise
    
    def create_task_breakdown(self, agent: Agent) -> Task:
        """
        Create the Task Breakdown task
        
        Args:
            agent: The agent responsible for this task
            
        Returns:
            Task configured for breaking down project into tasks
        """
        return Task(
            config=self.tasks_config['task_breakdown'],
            agent=agent
        )
    
    def create_time_resource_estimation(self, agent: Agent) -> Task:
        """
        Create the Time and Resource Estimation task
        
        Args:
            agent: The agent responsible for this task
            
        Returns:
            Task configured for estimating time and resources
        """
        return Task(
            config=self.tasks_config['time_resource_estimation'],
            agent=agent
        )
    
    def create_resource_allocation(
        self, 
        agent: Agent, 
        output_pydantic: Optional[type] = None
    ) -> Task:
        """
        Create the Resource Allocation task
        
        Args:
            agent: The agent responsible for this task
            output_pydantic: Pydantic model for structured output
            
        Returns:
            Task configured for resource allocation and milestone planning
        """
        task = Task(
            config=self.tasks_config['resource_allocation'],
            agent=agent
        )
        
        # Add structured output if provided
        if output_pydantic:
            task.output_pydantic = output_pydantic
        
        return task
    
    def get_all_tasks(
        self, 
        agents: list[Agent], 
        output_pydantic: Optional[type] = None
    ) -> list[Task]:
        """
        Create and return all tasks with assigned agents
        
        Args:
            agents: List of agents [planning_agent, estimation_agent, allocation_agent]
            output_pydantic: Pydantic model for final task output
            
        Returns:
            List of all configured tasks
        """
        if len(agents) != 3:
            raise ValueError("Expected 3 agents: [planning, estimation, allocation]")
        
        return [
            self.create_task_breakdown(agents[0]),
            self.create_time_resource_estimation(agents[1]),
            self.create_resource_allocation(agents[2], output_pydantic)
        ]


# Convenience function for quick task creation
def create_tasks(
    agents: list[Agent],
    output_pydantic: Optional[type] = None,
    config_path: str = "config/tasks.yaml"
) -> list[Task]:
    """
    Quick function to create all tasks
    
    Args:
        agents: List of agents for task assignment
        output_pydantic: Pydantic model for structured output
        config_path: Path to tasks configuration file
        
    Returns:
        List of all configured tasks
    """
    factory = ProjectTasks(config_path)
    return factory.get_all_tasks(agents, output_pydantic)