from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from config import Config
from bank_wrapper import bank_data
import json
from datetime import datetime

def get_all_goals():
    """Get all financial goals"""
    goals = bank_data.get_goals()
    return json.dumps(goals, indent=2)

def get_goal_progress(goal_name=None):
    """Get progress towards financial goals"""
    goals = bank_data.get_goals()
    
    if goal_name:
        goal = next((g for g in goals if goal_name.lower() in g["name"].lower()), None)
        if not goal:
            return json.dumps({"error": f"Goal '{goal_name}' not found"})
        goals = [goal]
    
    progress_data = []
    for goal in goals:
        progress_pct = (goal["current_amount"] / goal["target_amount"]) * 100
        remaining = goal["target_amount"] - goal["current_amount"]
        
        target_date = datetime.strptime(goal["target_date"], "%Y-%m-%d")
        days_remaining = (target_date - datetime.now()).days
        months_remaining = max(1, days_remaining / 30)
        
        monthly_needed = remaining / months_remaining if months_remaining > 0 else remaining
        
        progress_data.append({
            "goal_name": goal["name"],
            "target_amount": goal["target_amount"],
            "current_amount": goal["current_amount"],
            "progress_percentage": round(progress_pct, 1),
            "amount_remaining": round(remaining, 2),
            "target_date": goal["target_date"],
            "days_remaining": days_remaining,
            "monthly_savings_needed": round(monthly_needed, 2)
        })
    
    return json.dumps(progress_data, indent=2)

def calculate_savings_plan(target_amount, months):
    """Calculate monthly savings needed for a goal"""
    monthly_amount = target_amount / months
    
    plan = {
        "target_amount": target_amount,
        "time_period_months": months,
        "monthly_savings_needed": round(monthly_amount, 2),
        "weekly_savings_needed": round(monthly_amount / 4, 2),
        "total_to_save": target_amount
    }
    return json.dumps(plan, indent=2)

# Create the goals agent
goals_agent = LlmAgent(
    model=Config.MODEL_NAME,
    name="goals_specialist",
    description="Specialist agent for financial goals, savings targets, and future planning",
    instruction="""
    You are a financial goals specialist at Cymbal Bank. Your role is to help users set, 
    track, and achieve their financial goals through practical planning and advice.
    
    Your Capabilities:
    - Track progress towards savings goals
    - Calculate monthly savings requirements
    - Create realistic savings plans
    - Monitor goal timelines and milestones
    - Provide motivation and guidance
    
    When responding:
    1. Use the tools to get accurate goal data
    2. Break down large goals into manageable monthly amounts
    3. Celebrate progress and achievements
    4. Offer realistic timelines based on current savings rate
    5. Provide specific action steps
    6. Be encouraging and supportive
    
    If asked about topics outside financial goals, politely redirect to your area of expertise.
    """,
    tools=[
        FunctionTool(get_all_goals),
        FunctionTool(get_goal_progress),
        FunctionTool(calculate_savings_plan)
    ]
)