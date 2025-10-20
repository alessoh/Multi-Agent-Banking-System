import google.generativeai as genai
from config import Config
from bank_wrapper import bank_data
import json

# Configure Gemini
genai.configure(api_key=Config.GOOGLE_API_KEY)

def get_spending_summary():
    """Get a summary of recent spending by category"""
    spending = bank_data.get_spending_by_category(days=30)
    total = sum(spending.values())
    
    summary = {
        "total_spending_30_days": round(total, 2),
        "spending_by_category": {k: round(v, 2) for k, v in spending.items()},
        "top_category": max(spending.items(), key=lambda x: x[1])[0] if spending else None
    }
    return json.dumps(summary, indent=2)

def get_recent_transactions(limit=10):
    """Get recent transactions"""
    transactions = bank_data.get_transactions(days=30)
    recent = transactions[:limit]
    return json.dumps(recent, indent=2)

def get_monthly_trends():
    """Get spending trends over the last 3 months"""
    all_transactions = bank_data.get_transactions(days=90)
    
    months = {}
    for txn in all_transactions:
        month = txn["date"][:7]
        months[month] = months.get(month, 0) + txn["amount"]
    
    trends = {
        "monthly_totals": {k: round(v, 2) for k, v in sorted(months.items())},
        "average_monthly": round(sum(months.values()) / len(months), 2) if months else 0
    }
    return json.dumps(trends, indent=2)

class SpendingAgent:
    """Spending specialist agent"""
    
    def __init__(self):
        self.name = "spending_specialist"
        self.instruction = """
        You are a spending and transaction specialist at Cymbal Bank. Your role is to help users 
        understand their spending patterns, identify savings opportunities, and manage their budgets effectively.
        
        Your Capabilities:
        - Analyze spending by category
        - Identify spending trends over time
        - Suggest areas to reduce expenses
        - Provide insights on transaction patterns
        - Answer questions about recent purchases
        
        When responding:
        1. Use the data provided to give accurate spending information
        2. Provide specific numbers and percentages
        3. Offer actionable advice for saving money
        4. Be concise but thorough in your analysis
        5. Always maintain a helpful and encouraging tone
        
        If asked about something outside spending/transactions, politely explain your specialization.
        """
        
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            system_instruction=self.instruction
        )
        
        self.tools = {
            'get_spending_summary': get_spending_summary,
            'get_recent_transactions': get_recent_transactions,
            'get_monthly_trends': get_monthly_trends
        }
    
    def process_query(self, query):
        """Process a user query"""
        try:
            # Get all data upfront
            spending_data = get_spending_summary()
            transactions = get_recent_transactions()
            trends = get_monthly_trends()
            
            # Create context with data
            context = f"""
User Query: {query}

Available Data:

Spending Summary:
{spending_data}

Recent Transactions:
{transactions}

Monthly Trends:
{trends}

Please provide a helpful response based on this data. Be specific and actionable.
"""
            
            response = self.model.generate_content(context)
            return response.text
            
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Create the agent instance
spending_agent = SpendingAgent()