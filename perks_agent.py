from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from config import Config
from bank_wrapper import bank_data
import json

def get_all_perks():
    """Get all available banking perks"""
    perks = bank_data.get_perks()
    return json.dumps(perks, indent=2)

def get_active_perks():
    """Get currently active perks"""
    perks = bank_data.get_perks()
    active = [p for p in perks if p["status"] == "active"]
    return json.dumps(active, indent=2)

def get_available_perks():
    """Get perks available to activate"""
    perks = bank_data.get_perks()
    available = [p for p in perks if p["status"] == "available"]
    return json.dumps(available, indent=2)

def calculate_total_savings():
    """Calculate total potential savings from all perks"""
    perks = bank_data.get_perks()
    
    active_savings = sum(p["estimated_savings"] for p in perks if p["status"] == "active")
    potential_savings = sum(p["estimated_savings"] for p in perks if p["status"] == "available")
    total_possible = active_savings + potential_savings
    
    summary = {
        "current_monthly_savings": round(active_savings, 2),
        "potential_additional_savings": round(potential_savings, 2),
        "total_possible_savings": round(total_possible, 2),
        "active_perks_count": len([p for p in perks if p["status"] == "active"]),
        "available_perks_count": len([p for p in perks if p["status"] == "available"])
    }
    return json.dumps(summary, indent=2)

def get_perks_by_category(category):
    """Get perks for a specific spending category"""
    perks = bank_data.get_perks()
    filtered = [p for p in perks if category.lower() in p["category"].lower()]
    
    if not filtered:
        return json.dumps({"message": f"No perks found for category: {category}"})
    
    return json.dumps(filtered, indent=2)

# Create the perks agent
perks_agent = LlmAgent(
    model=Config.MODEL_NAME,
    name="perks_specialist",
    description="Specialist agent for banking perks, benefits, rewards, and account features",
    instruction="""
    You are a banking perks and benefits specialist at Cymbal Bank. Your role is to help users 
    maximize their savings and rewards through available perks and benefits.
    
    Your Capabilities:
    - Show all available perks and rewards
    - Calculate potential savings from perks
    - Recommend perks based on spending patterns
    - Explain perk terms and conditions
    - Help activate beneficial perks
    
    When responding:
    1. Use the tools to get accurate perk information
    2. Highlight the most valuable perks first
    3. Calculate and show potential savings in dollars
    4. Make personalized recommendations based on user spending
    5. Explain how to maximize each perk
    6. Be enthusiastic about helping users save money
    
    If asked about topics outside perks/benefits, politely redirect to your area of expertise.
    """,
    tools=[
        FunctionTool(get_all_perks),
        FunctionTool(get_active_perks),
        FunctionTool(get_available_perks),
        FunctionTool(calculate_total_savings),
        FunctionTool(get_perks_by_category)
    ]
)