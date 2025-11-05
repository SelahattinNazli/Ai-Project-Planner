"""
Main entry point for AI Project Planner
Demonstrates the usage of the project planning system
"""

import warnings
warnings.filterwarnings('ignore')

from helper import load_env
from src import ProjectPlannerCrew, ProjectPlan
import json
from pathlib import Path

# Load environment variables
load_env()


def print_separator(title: str = ""):
    """Print a nice separator with optional title"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}\n")


def save_results(result: ProjectPlan, output_dir: str = "outputs"):
    """
    Save planning results to JSON file
    
    Args:
        result: ProjectPlan object
        output_dir: Directory to save results
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(exist_ok=True)
    
    # Convert to dict and save
    result_dict = result.dict()
    output_file = Path(output_dir) / "project_plan.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Results saved to: {output_file}")


def display_results(result: ProjectPlan):
    """
    Display planning results in a formatted way
    
    Args:
        result: ProjectPlan object
    """
    print_separator("📋 PROJECT PLANNING RESULTS")
    
    # Display tasks
    print("🎯 TASKS:")
    print(f"Total tasks: {len(result.tasks)}\n")
    
    total_hours = 0
    for i, task in enumerate(result.tasks, 1):
        print(f"{i}. {task.task_name}")
        print(f"   ⏱️  Estimated Time: {task.estimated_time_hours} hours")
        print(f"   👥 Required Resources: {', '.join(task.required_resources)}")
        print()
        total_hours += task.estimated_time_hours
    
    print(f"⏰ Total Estimated Time: {total_hours} hours ({total_hours/8:.1f} days)\n")
    
    print_separator("🎯 MILESTONES")
    
    for i, milestone in enumerate(result.milestones, 1):
        print(f"{i}. {milestone.milestone_name}")
        print(f"   📌 Tasks: {len(milestone.tasks)}")
        for task in milestone.tasks:
            print(f"      • {task}")
        print()


def example_website_project():
    """Example: Website project planning"""
    
    print_separator("🚀 WEBSITE PROJECT PLANNING")
    
    # Project inputs
    project_type = "Website"
    industry = "Technology"
    project_objectives = "Create a modern, responsive website for a small business"
    
    team_members = """
    - John Doe (Project Manager)
    - Jane Smith (Full-stack Developer)
    - Bob Wilson (UI/UX Designer)
    - Alice Johnson (QA Engineer)
    """
    
    project_requirements = """
    - Responsive design for desktop, tablet, and mobile
    - Modern UI with clean, professional look
    - User-friendly navigation system
    - About Us page with company history
    - Services page showcasing offerings
    - Contact page with form and map
    - Blog section for news and updates
    - Fast loading times and SEO optimization
    - Social media integration
    - Customer testimonials section
    """
    
    # Display input information
    print(f"📊 Project Type: {project_type}")
    print(f"🏢 Industry: {industry}")
    print(f"🎯 Objectives: {project_objectives}")
    print(f"\n👥 Team Members:{team_members}")
    
    # Create crew and plan project
    crew = ProjectPlannerCrew(verbose=True)
    
    inputs = {
        'project_type': project_type,
        'project_objectives': project_objectives,
        'industry': industry,
        'team_members': team_members,
        'project_requirements': project_requirements
    }
    
    try:
        result = crew.plan_project(inputs)
        
        # Display results
        display_results(result)
        
        # Save results
        save_results(result)
        
        # Display metrics if available
        metrics = crew.get_usage_metrics()
        if metrics:
            print_separator("📊 USAGE METRICS")
            print(f"Total Tokens: {metrics['total_tokens']:,}")
            print(f"Prompt Tokens: {metrics['prompt_tokens']:,}")
            print(f"Completion Tokens: {metrics['completion_tokens']:,}")
            print(f"Successful Requests: {metrics['successful_requests']}")
            
            # Calculate cost (for Ollama it's free, but show for reference)
            cost = crew.calculate_cost()
            print(f"\n💰 Estimated Cost (if using paid API): ${cost:.4f}")
            print("💡 Note: Using Ollama (free local model)")
        
        print_separator("✅ PROJECT PLANNING COMPLETED")
        
        return result
        
    except Exception as e:
        print(f"\n❌ Error during planning: {str(e)}")
        raise


def example_mobile_app_project():
    """Example: Mobile app project planning"""
    
    print_separator("📱 MOBILE APP PROJECT PLANNING")
    
    inputs = {
        'project_type': 'Mobile Application',
        'project_objectives': 'Build a fitness tracking mobile app for iOS and Android',
        'industry': 'Health & Fitness',
        'team_members': """
        - Sarah Lee (Product Manager)
        - Mike Chen (iOS Developer)
        - Emma Davis (Android Developer)
        - Tom Brown (Backend Developer)
        - Lisa Wang (UI/UX Designer)
        """,
        'project_requirements': """
        - Native iOS and Android applications
        - User authentication and profiles
        - Workout tracking with GPS
        - Calorie and nutrition logging
        - Progress charts and statistics
        - Social features (friends, challenges)
        - Push notifications
        - Wearable device integration
        - Offline mode support
        - Cloud data synchronization
        """
    }
    
    crew = ProjectPlannerCrew(verbose=True)
    result = crew.plan_project(inputs)
    
    display_results(result)
    save_results(result, output_dir="outputs/mobile_app")
    
    return result


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          🤖 AI PROJECT PLANNER - Demo Script 🤖          ║
    ║                                                           ║
    ║     Powered by CrewAI + Ollama (qwen3:1.7b)             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Choose example to run
    print("Select an example to run:")
    print("1. Website Project (default)")
    print("2. Mobile App Project")
    print()
    
    choice = input("Enter choice (1 or 2, press Enter for default): ").strip()
    
    try:
        if choice == "2":
            result = example_mobile_app_project()
        else:
            result = example_website_project()
        
        print("\n✨ Demo completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        raise
