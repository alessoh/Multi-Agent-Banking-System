from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from config import Config
from bank_wrapper import bank_data
import json

def get_all_advisors():
    """Get all financial advisors"""
    advisors = bank_data.get_advisors()
    return json.dumps(advisors, indent=2)

def find_advisor_by_specialty(specialty):
    """Find advisors by their specialty"""
    advisors = bank_data.get_advisors()
    matches = [a for a in advisors if specialty.lower() in a["specialty"].lower()]
    
    if not matches:
        return json.dumps({"message": f"No advisors found with specialty: {specialty}"})
    
    return json.dumps(matches, indent=2)

def get_advisor_details(advisor_name):
    """Get details for a specific advisor"""
    advisors = bank_data.get_advisors()
    advisor = next((a for a in advisors if advisor_name.lower() in a["name"].lower()), None)
    
    if not advisor:
        return json.dumps({"error": f"Advisor '{advisor_name}' not found"})
    
    return json.dumps(advisor, indent=2)

def recommend_advisor(user_need):
    """Recommend an advisor based on user's financial need"""
    advisors = bank_data.get_advisors()
    
    # Simple keyword matching for recommendations
    keywords = {
        "retirement": "Retirement Planning",
        "invest": "Investment Strategy",
        "debt": "Debt Management",
        "save": "Investment Strategy",
        "loan": "Debt Management"
    }
    
    specialty = None
    for keyword, spec in keywords.items():
        if keyword in user_need.lower():
            specialty = spec
            break
    
    if specialty:
        matches = [a for a in advisors if specialty in a["specialty"]]
        if matches:
            recommendation = {
                "recommended_advisor": matches[0],
                "reason": f"Best match for your need: {user_need}",
                "other_options": matches[1:] if len(matches) > 1 else []
            }
            return json.dumps(recommendation, indent=2)
    
    # Default: return all advisors
    return json.dumps({
        "message": "Here are all available advisors",
        "advisors": advisors
    }, indent=2)

# Create the advisors agent
advisors_agent = LlmAgent(
    model=Config.MODEL_NAME,
    name="advisors_specialist",
    description="Specialist agent for financial advisory services and advisor connections",
    instruction="""
    You are a financial advisory services specialist at Cymbal Bank. Your role is to connect 
    users with the right financial advisors based on their needs and goals.
    
    Your Capabilities:
    - Show available financial advisors
    - Match users with appropriate specialists
    - Provide advisor ratings and specialties
    - Explain what each advisor can help with
    - Help schedule advisory meetings
    
    When responding:
    1. Use the tools to get accurate advisor information
    2. Ask about the user's specific financial needs
    3. Recommend the most appropriate advisor
    4. Explain what users can expect from a meeting
    5. Highlight advisor specialties and ratings
    6. Be professional and reassuring
    
    If asked about topics outside advisory services, politely redirect to your specialty.
    """,
    tools=[
        FunctionTool(get_all_advisors),
        FunctionTool(find_advisor_by_specialty),
        FunctionTool(get_advisor_details),
        FunctionTool(recommend_advisor)
    ]
)