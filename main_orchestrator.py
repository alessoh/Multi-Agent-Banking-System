import google.generativeai as genai
from config import Config

# Configure Gemini
genai.configure(api_key=Config.GOOGLE_API_KEY)

# Import all specialist agents
from spending_agent import spending_agent
from goals_agent import goals_agent
from portfolio_agent import portfolio_agent
from perks_agent import perks_agent
from advisors_agent import advisors_agent

class ChatOrchestrator:
    """Main chat orchestrator that routes queries to specialist agents"""
    
    def __init__(self):
        self.name = "chat_orchestrator"
        self.instruction = """
        You are an intelligent banking assistant orchestrator for Cymbal Bank. Your role is to 
        understand user queries and route them to the appropriate specialist agent.
        
        AVAILABLE SPECIALIST AGENTS:
        
        1. SPENDING - For: transactions, expenses, budgets, spending patterns
        2. GOALS - For: savings goals, targets, progress, savings plans
        3. PORTFOLIO - For: investments, net worth, debt, asset allocation
        4. PERKS - For: rewards, cashback, benefits, offers
        5. ADVISORS - For: connecting with financial advisors, scheduling meetings
        
        Analyze the query and respond with ONLY ONE WORD indicating which specialist to use:
        - "SPENDING" for spending/transaction questions
        - "GOALS" for savings goal questions
        - "PORTFOLIO" for investment/debt questions
        - "PERKS" for rewards/benefits questions
        - "ADVISORS" for advisor/meeting questions
        
        If unclear, respond with "SPENDING" as the default.
        """
        
        self.model = genai.GenerativeModel(
            model_name=Config.MODEL_NAME,
            system_instruction=self.instruction
        )
        
        self.agents = {
            'SPENDING': spending_agent,
            'GOALS': goals_agent,
            'PORTFOLIO': portfolio_agent,
            'PERKS': perks_agent,
            'ADVISORS': advisors_agent
        }
    
    def process_query(self, query):
        """Process a user query by routing to the right specialist"""
        try:
            # Determine which agent to use
            routing_prompt = f"User query: {query}\n\nWhich specialist should handle this?"
            routing_response = self.model.generate_content(routing_prompt)
            
            # Extract the agent name from response
            agent_name = routing_response.text.strip().upper()
            
            # Clean up the response to just get the agent name
            for key in self.agents.keys():
                if key in agent_name:
                    agent_name = key
                    break
            
            # Default to spending if no match
            if agent_name not in self.agents:
                agent_name = 'SPENDING'
            
            # Route to the appropriate agent
            selected_agent = self.agents[agent_name]
            response = selected_agent.process_query(query)
            
            return response
            
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Create the orchestrator instance
root_agent = ChatOrchestrator()