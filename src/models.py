"""
Pydantic models for structured output from AI agents.
Defines the schema for project planning results.
"""

from typing import List
from pydantic import BaseModel, Field


class TaskEstimate(BaseModel):
    """Model for individual task estimation"""
    
    task_name: str = Field(
        ..., 
        description="Name of the task"
    )
    estimated_time_hours: float = Field(
        ..., 
        description="Estimated time to complete the task in hours"
    )
    required_resources: List[str] = Field(
        ..., 
        description="List of resources required to complete the task"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_name": "Design homepage mockup",
                "estimated_time_hours": 8.0,
                "required_resources": ["UI Designer", "Figma"]
            }
        }


class Milestone(BaseModel):
    """Model for project milestones"""
    
    milestone_name: str = Field(
        ..., 
        description="Name of the milestone"
    )
    tasks: List[str] = Field(
        ..., 
        description="List of task names associated with this milestone"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "milestone_name": "MVP Launch",
                "tasks": ["Design homepage", "Implement authentication", "Deploy to staging"]
            }
        }


class ProjectPlan(BaseModel):
    """Complete project plan with tasks and milestones"""
    
    tasks: List[TaskEstimate] = Field(
        ..., 
        description="List of tasks with their estimates"
    )
    milestones: List[Milestone] = Field(
        ..., 
        description="List of project milestones"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "task_name": "Design homepage",
                        "estimated_time_hours": 8.0,
                        "required_resources": ["UI Designer"]
                    }
                ],
                "milestones": [
                    {
                        "milestone_name": "MVP Launch",
                        "tasks": ["Design homepage", "Setup database"]
                    }
                ]
            }
        }