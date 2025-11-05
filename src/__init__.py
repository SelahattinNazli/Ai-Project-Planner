"""
AI Project Planner - CrewAI based project planning system

This package provides AI-powered project planning capabilities using
multiple specialized agents working together as a crew.

Main Components:
    - Agents: Specialized AI agents for different planning tasks
    - Tasks: Configurable tasks for the agents to perform
    - Models: Pydantic models for structured output
    - Crew: Orchestration layer that coordinates agents and tasks

Usage:
    from src import ProjectPlannerCrew, plan_project
    
    # Quick planning
    result = plan_project(
        project_type="Website",
        project_objectives="Build an e-commerce site",
        industry="Retail",
        team_members="3 developers, 1 designer",
        project_requirements="Shopping cart, payment integration..."
    )
    
    # Detailed control
    crew = ProjectPlannerCrew(verbose=True)
    result = crew.plan_project(inputs)
"""

__version__ = "0.1.0"
__author__ = "AI Project Planner Team"

# Import main classes and functions for easy access
from .agents import ProjectAgents, create_agents
from .tasks import ProjectTasks, create_tasks
from .models import TaskEstimate, Milestone, ProjectPlan
from .crew import ProjectPlannerCrew, plan_project

# Define what gets imported with "from src import *"
__all__ = [
    # Main orchestration
    "ProjectPlannerCrew",
    "plan_project",
    
    # Agent management
    "ProjectAgents",
    "create_agents",
    
    # Task management
    "ProjectTasks", 
    "create_tasks",
    
    # Data models
    "TaskEstimate",
    "Milestone",
    "ProjectPlan",
    
    # Package metadata
    "__version__",
    "__author__",
]

# Package initialization message
print(f"🤖 AI Project Planner v{__version__} loaded successfully!")