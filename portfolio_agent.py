import google.generativeai as genai
from config import Config
from bank_wrapper import bank_data
import json

# Configure Gemini
genai.configure(api_key=Config.GOOGLE_API_KEY)

def get_portfolio_summary():
    """Get investment portfolio summary"""
    investments = bank_data.get_investments()
    return json.dumps(investments, indent=2)

def get_net_worth():
    """Get net worth calculation"""
    net_worth = bank_data.get_net_worth()
    return json.dumps(net_worth, indent=2)

def get_debt_summary():
    """Get summary of all debts"""
    debts = bank_data.get_debts()
    total_debt = sum(debt["balance"] for debt in debts)
    total_minimum = sum(debt["minimum_payment"] for debt in debts)
    
    summary = {
        "total_debt": round(total_debt, 2),
        "total_minimum_payment": round(total_minimum, 2),
        "debts": debts
    }
    return json.dumps(summary, indent=2)

def calculate_debt_payoff_strategies():
    """Calculate debt payoff strategies"""
    debts = bank_data.get_debts()
    
    avalanche = sorted(debts, key=lambda x: x["interest_rate"], reverse=True)
    snowball = sorted(debts, key=lambda x: x["balance"])
    
    strategies = {
        "avalanche_method": {
            "description": "Pay off highest interest rate debts first (saves most money)",
            "order": [{"type": d["type"], "balance": d["balance"], "rate": d["interest_rate"]} for d in avalanche]
        },
        "snowball_method": {
            "description": "Pay off lowest balance debts first (psychological wins)",
            "order": [{"type": d["type"], "balance": d["balance"], "rate": d["interest_rate"]} for d in snowball]
        }
    }
    return json.dumps(strategies, indent=2)

def analyze_asset_allocation():
    """Analyze current asset allocation"""
    investments = bank_data.get_investments()
    holdings = investments["holdings"]
    
    analysis = {
        "current_allocation": holdings,
        "total_value": investments["total_value"],
        "diversification_score": len(holdings),
        "performance": investments["performance"]
    }
    return json.dumps(analysis, indent=2)

class PortfolioAgent:
    """Investment portfolio specialist agent"""
    
    def __init__(self):
        self.name = "portfolio_specialist"
        self.instruction = """
        You are an investment portfolio specialist at Cymbal Bank. Your role is to help users 
        understand their investments, manage debt, and build wealth through informed decisions.
        
        Your Capabilities:
        - Analyze investment portfolio performance
        - Calculate net worth
        - Provide debt payoff strategies
        - Assess asset allocation
        - Offer portfolio diversification advice
        
        When responding:
        1. Use the data to access accurate financial information
        2. Explain complex financial concepts in simple terms
        3. Provide specific recommendations with rationale
        4. Compare different strategies (e.g., avalanche vs snowball for debt)
        5. Focus on long-term wealth building
        6. Always note that you provide general guidance, not personalized financial advice
        
        If asked about topics outside investments/debt/portfolio, politely redirect to your specialty.
        """
        
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            system_instruction=self.instruction
        )
    
    def process_query(self, query):
        """Process a user query"""
        try:
            # Get all portfolio data
            portfolio_data = get_portfolio_summary()
            net_worth_data = get_net_worth()
            debt_data = get_debt_summary()
            strategies = calculate_debt_payoff_strategies()
            allocation = analyze_asset_allocation()
            
            # Create context with data
            context = f"""
User Query: {query}

Available Data:

Portfolio Summary:
{portfolio_data}

Net Worth:
{net_worth_data}

Debt Summary:
{debt_data}

Debt Payoff Strategies:
{strategies}

Asset Allocation Analysis:
{allocation}

Please provide a helpful response based on this data. Be specific and educational.
"""
            
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error in PortfolioAgent: {error_details}")
            return f"Error processing query: {str(e)}"

# Create the agent instance
portfolio_agent = PortfolioAgent()