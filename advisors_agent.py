import google.generativeai as genai
from config import Config
from bank_wrapper import bank_data
import json

# Configure Gemini
genai.configure(api_key=Config.GOOGLE_API_KEY)

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

def recommend_advisor(user_need):
    """Recommend an advisor based on user's financial need"""
    advisors = bank_data.get_advisors()
    
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
    
    return json.dumps({
        "message": "Here are all available advisors",
        "advisors": advisors
    }, indent=2)

class AdvisorsAgent:
    """Financial advisory services specialist agent"""
    
    def __init__(self):
        self.name = "advisors_specialist"
        self.instruction = """
        You are a financial advisory services specialist at Cymbal Bank. Your role is to connect 
        users with the right financial advisors based on their needs and goals.
        
        Your Capabilities:
        - Show available financial advisors
        - Match users with appropriate specialists
        - Provide advisor ratings and specialties
        - Explain what each advisor can help with
        - Help schedule advisory meetings
        
        When responding:
        1. Use the data to get accurate advisor information
        2. Ask about the user's specific financial needs
        3. Recommend the most appropriate advisor
        4. Explain what users can expect from a meeting
        5. Highlight advisor specialties and ratings
        6. Be professional and reassuring
        
        If asked about topics outside advisory services, politely redirect to your specialty.
        """
        
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            system_instruction=self.instruction
        )
    
    def process_query(self, query):
        """Process a user query"""
        try:
            # Get all advisors data
            advisors = get_all_advisors()
            recommendation = recommend_advisor(query)
            
            # Create context with data
            context = f"""
User Query: {query}

Available Data:

All Advisors:
{advisors}

Recommendation Based on Query:
{recommendation}

Please provide a helpful response based on this data. Be professional and helpful.
"""
            
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in AdvisorsAgent: {error_details}")
            return f"Error processing query: {str(e)}"

# Create the agent instance
advisors_agent = AdvisorsAgent()