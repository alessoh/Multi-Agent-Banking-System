import google.generativeai as genai
from config import Config
from bank_wrapper import bank_data
import json

# Configure Gemini
genai.configure(api_key=Config.GOOGLE_API_KEY)

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

class PerksAgent:
    """Banking perks specialist agent"""
    
    def __init__(self):
        self.name = "perks_specialist"
        self.instruction = """
        You are a banking perks and benefits specialist at Cymbal Bank. Your role is to help users 
        maximize their savings and rewards through available perks and benefits.
        
        Your Capabilities:
        - Show all available perks and rewards
        - Calculate potential savings from perks
        - Recommend perks based on spending patterns
        - Explain perk terms and conditions
        - Help activate beneficial perks
        
        When responding:
        1. Use the data to get accurate perk information
        2. Highlight the most valuable perks first
        3. Calculate and show potential savings in dollars
        4. Make personalized recommendations based on user spending
        5. Explain how to maximize each perk
        6. Be enthusiastic about helping users save money
        
        If asked about topics outside perks/benefits, politely redirect to your area of expertise.
        """
        
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            system_instruction=self.instruction
        )
    
    def process_query(self, query):
        """Process a user query"""
        try:
            # Get all perks data
            all_perks = get_all_perks()
            active = get_active_perks()
            available = get_available_perks()
            savings = calculate_total_savings()
            
            # Create context with data
            context = f"""
User Query: {query}

Available Data:

All Perks:
{all_perks}

Active Perks:
{active}

Available Perks:
{available}

Savings Calculation:
{savings}

Please provide a helpful response based on this data. Be enthusiastic about savings opportunities!
"""
            
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in PerksAgent: {error_details}")
            return f"Error processing query: {str(e)}"

# Create the agent instance
perks_agent = PerksAgent()