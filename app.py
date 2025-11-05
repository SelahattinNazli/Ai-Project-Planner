"""
Streamlit Web Application for AI Project Planner
Beautiful, interactive interface for project planning with AI
"""

import streamlit as st
import warnings
warnings.filterwarnings('ignore')

from helper import load_env
from src import ProjectPlannerCrew, ProjectPlan
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Load environment variables
load_env()

# Page configuration
st.set_page_config(
    page_title="AI Project Planner",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'planning_result' not in st.session_state:
        st.session_state.planning_result = None
    if 'crew' not in st.session_state:
        st.session_state.crew = None
    if 'planning_complete' not in st.session_state:
        st.session_state.planning_complete = False


def create_gantt_chart(tasks_df: pd.DataFrame):
    """
    Create a Gantt chart from tasks dataframe
    
    Args:
        tasks_df: DataFrame with tasks information
    """
    # Calculate start and end dates
    start_date = datetime.now()
    
    gantt_data = []
    current_date = start_date
    
    for _, task in tasks_df.iterrows():
        end_date = current_date + timedelta(hours=task['estimated_time_hours'])
        gantt_data.append({
            'Task': task['task_name'],
            'Start': current_date,
            'Finish': end_date,
            'Resources': ', '.join(task['required_resources']) if isinstance(task['required_resources'], list) else task['required_resources']
        })
        current_date = end_date
    
    gantt_df = pd.DataFrame(gantt_data)
    
    fig = px.timeline(
        gantt_df,
        x_start='Start',
        x_end='Finish',
        y='Task',
        title='Project Timeline (Gantt Chart)',
        color='Resources',
        hover_data=['Resources']
    )
    
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        height=max(400, len(gantt_df) * 40),
        xaxis_title="Timeline",
        yaxis_title="Tasks",
        showlegend=True
    )
    
    return fig


def create_resource_chart(tasks_df: pd.DataFrame):
    """
    Create resource allocation pie chart
    
    Args:
        tasks_df: DataFrame with tasks information
    """
    # Flatten resources list and count
    all_resources = []
    for resources in tasks_df['required_resources']:
        if isinstance(resources, list):
            all_resources.extend(resources)
        else:
            all_resources.append(resources)
    
    resource_counts = pd.Series(all_resources).value_counts()
    
    fig = px.pie(
        values=resource_counts.values,
        names=resource_counts.index,
        title='Resource Allocation Distribution',
        hole=0.4
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig


def create_time_distribution_chart(tasks_df: pd.DataFrame):
    """
    Create time distribution bar chart
    
    Args:
        tasks_df: DataFrame with tasks information
    """
    fig = px.bar(
        tasks_df,
        x='task_name',
        y='estimated_time_hours',
        title='Time Distribution by Task',
        labels={'task_name': 'Task', 'estimated_time_hours': 'Hours'},
        color='estimated_time_hours',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500
    )
    
    return fig


def export_to_json(result: ProjectPlan):
    """Export results to JSON format"""
    return json.dumps(result.dict(), indent=2, ensure_ascii=False)


def export_to_csv(tasks_df: pd.DataFrame):
    """Export tasks to CSV format"""
    return tasks_df.to_csv(index=False).encode('utf-8')


def main():
    """Main Streamlit application"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Project Planner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your ideas into actionable project plans with AI-powered planning</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/3d-fluency/200/artificial-intelligence.png", width=150)
        st.title("⚙️ Configuration")
        
        st.info("💡 **Using Ollama (qwen3:1.7b)**\n\nFree local AI model for project planning")
        
        st.divider()
        
        st.markdown("### 📊 About")
        st.markdown("""
        This AI-powered tool uses **CrewAI** with multiple specialized agents to:
        
        - 📋 Break down projects into tasks
        - ⏱️ Estimate time and resources
        - 👥 Allocate team members
        - 🎯 Create milestones
        
        Powered by **Ollama** (100% free!)
        """)
        
        st.divider()
        
        if st.button("🔄 Reset Application"):
            st.session_state.planning_result = None
            st.session_state.crew = None
            st.session_state.planning_complete = False
            st.rerun()
    
    # Main content
    if not st.session_state.planning_complete:
        # Input Form
        st.markdown("### 📝 Project Information")
        
        st.info("💡 **Tip:** Fill in all fields with your project details. You can plan ANY type of project!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_type = st.text_input(
                "Project Type *",
                value="",
                placeholder="e.g., Website, Mobile App, API, SaaS Platform, CRM System...",
                help="Enter any type of project you want to plan"
            )
            
            industry = st.text_input(
                "Industry *",
                value="",
                placeholder="e.g., Technology, Healthcare, Finance, E-commerce, Education...",
                help="Enter the industry domain of your project"
            )
            
            project_objectives = st.text_area(
                "Project Objectives *",
                value="",
                placeholder="Example:\n- Increase user engagement by 40%\n- Reduce operational costs\n- Launch MVP within 3 months\n- Build a scalable platform...",
                height=120,
                help="Describe the main goals and objectives of your project"
            )
        
        with col2:
            team_members = st.text_area(
                "Team Members *",
                value="",
                placeholder="Example:\n- John Doe (Project Manager)\n- Jane Smith (Full-stack Developer)\n- Bob Wilson (UI/UX Designer)\n- Alice Johnson (QA Engineer)\n- Tom Brown (DevOps Engineer)",
                height=180,
                help="List your team members and their roles (one per line)"
            )
        
        project_requirements = st.text_area(
            "Project Requirements *",
            value="",
            placeholder="Example:\n- User authentication and authorization\n- Responsive design for all devices\n- RESTful API integration\n- Real-time notifications\n- Payment gateway integration\n- Admin dashboard with analytics\n- Database optimization\n- Security compliance (GDPR, SSL)\n- Performance monitoring\n- Automated testing",
            height=250,
            help="Detailed list of project requirements, features, and technical specifications"
        )
        
        st.divider()
        
        # Example templates
        with st.expander("📌 Need inspiration? Click here for example templates"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🌐 Website Project**")
                if st.button("Use Template", key="web"):
                    st.session_state.template = {
                        'project_type': 'Business Website',
                        'industry': 'Technology',
                        'objectives': 'Create a modern, responsive website to showcase our services and attract clients',
                        'team': '- Project Manager\n- Full-stack Developer\n- UI/UX Designer\n- Content Writer',
                        'requirements': '- Responsive design\n- Contact form\n- Blog section\n- SEO optimization\n- Fast loading\n- Social media integration'
                    }
                    st.rerun()
            
            with col2:
                st.markdown("**📱 Mobile App**")
                if st.button("Use Template", key="mobile"):
                    st.session_state.template = {
                        'project_type': 'Mobile Application',
                        'industry': 'Health & Fitness',
                        'objectives': 'Build a fitness tracking app for iOS and Android users',
                        'team': '- Product Manager\n- iOS Developer\n- Android Developer\n- Backend Developer\n- UI/UX Designer',
                        'requirements': '- User authentication\n- Workout tracking\n- Progress charts\n- Social features\n- Push notifications\n- Offline mode'
                    }
                    st.rerun()
            
            with col3:
                st.markdown("**🛒 E-commerce**")
                if st.button("Use Template", key="ecommerce"):
                    st.session_state.template = {
                        'project_type': 'E-commerce Platform',
                        'industry': 'Retail',
                        'objectives': 'Launch an online store with secure payment and inventory management',
                        'team': '- Project Manager\n- Backend Developer\n- Frontend Developer\n- UI/UX Designer\n- QA Engineer',
                        'requirements': '- Product catalog\n- Shopping cart\n- Payment gateway\n- Order management\n- Inventory system\n- Admin dashboard'
                    }
                    st.rerun()
        
        # Apply template if selected
        if 'template' in st.session_state:
            template = st.session_state.template
            st.success("✅ Template loaded! You can now edit the fields above.")
            # Clear template after showing message
            del st.session_state.template
        
        st.divider()
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate Project Plan", use_container_width=True):
                # Validation
                if not all([project_type, industry, project_objectives, team_members, project_requirements]):
                    st.error("⚠️ Please fill in all required fields!")
                    st.warning("💡 All fields marked with * are required")
                    return
                
                # Show planning in progress
                with st.spinner("🤖 AI agents are planning your project... This may take 2-5 minutes."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Simulate progress
                        status_text.text("🔍 Analyzing project requirements...")
                        progress_bar.progress(20)
                        
                        # Create crew
                        crew = ProjectPlannerCrew(verbose=False)
                        st.session_state.crew = crew
                        
                        status_text.text("🤖 AI agents are working together...")
                        progress_bar.progress(40)
                        
                        # Prepare inputs
                        inputs = {
                            'project_type': project_type,
                            'project_objectives': project_objectives,
                            'industry': industry,
                            'team_members': team_members,
                            'project_requirements': project_requirements
                        }
                        
                        status_text.text("📋 Breaking down tasks...")
                        progress_bar.progress(60)
                        
                        # Plan project
                        result = crew.plan_project(inputs)
                        
                        status_text.text("⏱️ Estimating time and resources...")
                        progress_bar.progress(80)
                        
                        st.session_state.planning_result = result
                        st.session_state.planning_complete = True
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Planning complete!")
                        
                        st.success("🎉 Project plan generated successfully!")
                        st.balloons()
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred: {str(e)}")
                        st.exception(e)
                        progress_bar.empty()
                        status_text.empty()
    
    else:
        # Display Results
        result = st.session_state.planning_result
        crew = st.session_state.crew
        
        st.markdown("### 🎉 Project Plan Generated Successfully!")
        
        # Metrics
        total_hours = sum(task.estimated_time_hours for task in result.tasks)
        total_days = total_hours / 8
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📋 Total Tasks", len(result.tasks))
        with col2:
            st.metric("⏰ Total Hours", f"{total_hours:.1f}")
        with col3:
            st.metric("📅 Estimated Days", f"{total_days:.1f}")
        with col4:
            st.metric("🎯 Milestones", len(result.milestones))
        
        st.divider()
        
        # Tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Tasks", "🎯 Milestones", "📊 Visualizations", "💾 Export"])
        
        with tab1:
            st.markdown("### 📋 Task Breakdown")
            
            # Convert to DataFrame
            tasks_data = []
            for task in result.tasks:
                tasks_data.append({
                    'task_name': task.task_name,
                    'estimated_time_hours': task.estimated_time_hours,
                    'required_resources': ', '.join(task.required_resources) if isinstance(task.required_resources, list) else task.required_resources
                })
            
            tasks_df = pd.DataFrame(tasks_data)
            
            # Display as interactive table
            st.dataframe(
                tasks_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "task_name": st.column_config.TextColumn("Task Name", width="large"),
                    "estimated_time_hours": st.column_config.NumberColumn("Hours", format="%.1f"),
                    "required_resources": st.column_config.TextColumn("Resources", width="medium")
                }
            )
            
            # Detailed task cards
            st.markdown("#### 📄 Detailed View")
            for i, task in enumerate(result.tasks, 1):
                with st.expander(f"{i}. {task.task_name}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**⏱️ Estimated Time:** {task.estimated_time_hours} hours")
                    with col2:
                        st.markdown(f"**👥 Required Resources:**")
                        for resource in task.required_resources:
                            st.markdown(f"- {resource}")
        
        with tab2:
            st.markdown("### 🎯 Project Milestones")
            
            for i, milestone in enumerate(result.milestones, 1):
                with st.container():
                    st.markdown(f"#### {i}. {milestone.milestone_name}")
                    
                    st.markdown(f"**📌 Tasks in this milestone:** {len(milestone.tasks)}")
                    
                    for task in milestone.tasks:
                        st.markdown(f"- {task}")
                    
                    st.divider()
        
        with tab3:
            st.markdown("### 📊 Project Visualizations")
            
            # Time Distribution Chart
            st.plotly_chart(create_time_distribution_chart(tasks_df), use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Resource Allocation Chart
                st.plotly_chart(create_resource_chart(tasks_df), use_container_width=True)
            
            with col2:
                # Gantt Chart
                st.plotly_chart(create_gantt_chart(tasks_df), use_container_width=True)
        
        with tab4:
            st.markdown("### 💾 Export Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📄 Export to JSON")
                json_data = export_to_json(result)
                st.download_button(
                    label="⬇️ Download JSON",
                    data=json_data,
                    file_name=f"project_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                with st.expander("👁️ Preview JSON"):
                    st.json(result.dict())
            
            with col2:
                st.markdown("#### 📊 Export to CSV")
                csv_data = export_to_csv(tasks_df)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"project_tasks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
                with st.expander("👁️ Preview CSV"):
                    st.dataframe(tasks_df)
        
        # Usage Metrics (if available)
        if crew:
            metrics = crew.get_usage_metrics()
            if metrics:
                with st.expander("📊 Usage Metrics & Performance"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Tokens", f"{metrics['total_tokens']:,}")
                    with col2:
                        st.metric("Prompt Tokens", f"{metrics['prompt_tokens']:,}")
                    with col3:
                        st.metric("Completion Tokens", f"{metrics['completion_tokens']:,}")
                    
                    st.info("💡 Using Ollama - Completely Free! No API costs.")


if __name__ == "__main__":
    main()