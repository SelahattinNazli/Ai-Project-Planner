"""
Crew orchestration for AI Project Planner.
Manages the coordination of agents and tasks.
"""

from crewai import Crew
from typing import Dict, Any, Optional
from pathlib import Path

from .agents import ProjectAgents
from .tasks import ProjectTasks
from .models import ProjectPlan


class ProjectPlannerCrew:
    """Main crew orchestrator for project planning"""
    
    def __init__(
        self,
        agents_config: str = "config/agents.yaml",
        tasks_config: str = "config/tasks.yaml",
        verbose: bool = True
    ):
        """
        Initialize the project planner crew
        
        Args:
            agents_config: Path to agents configuration
            tasks_config: Path to tasks configuration
            verbose: Enable verbose output
        """
        self.verbose = verbose
        
        # Initialize factories
        self.agents_factory = ProjectAgents(agents_config)
        self.tasks_factory = ProjectTasks(tasks_config)
        
        # Create agents
        self.agents = self.agents_factory.get_all_agents()
        
        # Create tasks with structured output
        self.tasks = self.tasks_factory.get_all_tasks(
            self.agents,
            output_pydantic=ProjectPlan
        )
        
        # Create crew
        self.crew = Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=self.verbose
        )
        
        print("✅ Project Planner Crew initialized successfully!")
    
    def plan_project(self, inputs: Dict[str, Any]) -> ProjectPlan:
        """
        Execute project planning with given inputs
        
        Args:
            inputs: Dictionary containing:
                - project_type: Type of project (e.g., "Website", "Mobile App")
                - project_objectives: Main objectives of the project
                - industry: Industry domain
                - team_members: List or description of team members
                - project_requirements: Detailed requirements
        
        Returns:
            ProjectPlan object with structured results
        """
        # Validate inputs
        required_keys = [
            'project_type',
            'project_objectives', 
            'industry',
            'team_members',
            'project_requirements'
        ]
        
        missing_keys = [key for key in required_keys if key not in inputs]
        if missing_keys:
            raise ValueError(f"Missing required input keys: {missing_keys}")
        
        print("\n🚀 Starting project planning process...")
        print(f"📋 Project Type: {inputs['project_type']}")
        print(f"🏢 Industry: {inputs['industry']}\n")
        
        # Execute crew
        result = self.crew.kickoff(inputs=inputs)
        
        print("\n✅ Project planning completed!")
        
        return result.pydantic
    
    def get_usage_metrics(self) -> Optional[Dict[str, Any]]:
        """
        Get usage metrics from the crew execution
        
        Returns:
            Dictionary with usage metrics or None if not available
        """
        if hasattr(self.crew, 'usage_metrics'):
            metrics = self.crew.usage_metrics
            return {
                'total_tokens': metrics.total_tokens,
                'prompt_tokens': metrics.prompt_tokens,
                'completion_tokens': metrics.completion_tokens,
                'successful_requests': metrics.successful_requests
            }
        return None
    
    def calculate_cost(self, cost_per_million: float = 0.150) -> float:
        """
        Calculate estimated cost based on token usage
        
        Args:
            cost_per_million: Cost per million tokens (default for GPT-4)
        
        Returns:
            Estimated cost in dollars
        """
        metrics = self.get_usage_metrics()
        if metrics:
            total_tokens = metrics['total_tokens']
            return (cost_per_million * total_tokens) / 1_000_000
        return 0.0


# Convenience function for quick crew creation and execution
def plan_project(
    project_type: str,
    project_objectives: str,
    industry: str,
    team_members: str,
    project_requirements: str,
    verbose: bool = True
) -> ProjectPlan:
    """
    Quick function to plan a project
    
    Args:
        project_type: Type of project
        project_objectives: Main objectives
        industry: Industry domain
        team_members: Team members description
        project_requirements: Detailed requirements
        verbose: Enable verbose output
    
    Returns:
        ProjectPlan with structured results
    """
    crew = ProjectPlannerCrew(verbose=verbose)
    
    inputs = {
        'project_type': project_type,
        'project_objectives': project_objectives,
        'industry': industry,
        'team_members': team_members,
        'project_requirements': project_requirements
    }
    
    return crew.plan_project(inputs)