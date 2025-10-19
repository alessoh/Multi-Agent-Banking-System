from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from config import Config
from bank_wrapper import bank_data
import json

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
    """Calculate debt payoff strategies (avalanche and snowball)"""
    debts = bank_data.get_debts()
    
    # Avalanche method (highest interest rate first)
    avalanche = sorted(debts, key=lambda x: x["interest_rate"], reverse=True)
    
    # Snowball method (lowest balance first)
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
        "performance": investments["performance"],
        "recommendation": "Your portfolio shows good diversification across asset classes."
    }
    return json.dumps(analysis, indent=2)

# Create the portfolio agent
portfolio_agent = LlmAgent(
    model=Config.MODEL_NAME,
    name="portfolio_specialist",
    description="Specialist agent for investment portfolios, debt management, and net worth analysis",
    instruction="""
    You are an investment portfolio specialist at Cymbal Bank. Your role is to help users 
    understand their investments, manage debt, and build wealth through informed decisions.
    
    Your Capabilities:
    - Analyze investment portfolio performance
    - Calculate net worth
    - Provide debt payoff strategies
    - Assess asset allocation
    - Offer portfolio diversification advice
    
    When responding:
    1. Use the tools to access accurate financial data
    2. Explain complex financial concepts in simple terms
    3. Provide specific recommendations with rationale
    4. Compare different strategies (e.g., avalanche vs snowball for debt)
    5. Focus on long-term wealth building
    6. Always note that you provide general guidance, not personalized financial advice
    
    If asked about topics outside investments/debt/portfolio, politely redirect to your specialty.
    """,
    tools=[
        FunctionTool(get_portfolio_summary),
        FunctionTool(get_net_worth),
        FunctionTool(get_debt_summary),
        FunctionTool(calculate_debt_payoff_strategies),
        FunctionTool(analyze_asset_allocation)
    ]
)