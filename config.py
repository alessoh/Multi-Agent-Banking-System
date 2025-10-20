import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings
class Config:
    # API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_GENAI_USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")
    
    # Validate API key
    if not GOOGLE_API_KEY and GOOGLE_GENAI_USE_VERTEXAI != "TRUE":
        raise ValueError(
            "GOOGLE_API_KEY environment variable not set. "
            "Please add it to your .env file."
        )
    
    # Agent Ports
    SPENDING_AGENT_PORT = 8081
    PERKS_AGENT_PORT = 8082
    PORTFOLIO_AGENT_PORT = 8083
    GOALS_AGENT_PORT = 8084
    ADVISORS_AGENT_PORT = 8085
    CHAT_ORCHESTRATOR_PORT = 8090
    
    # Agent URLs
    SPENDING_AGENT_URL = f"http://localhost:{SPENDING_AGENT_PORT}"
    PERKS_AGENT_URL = f"http://localhost:{PERKS_AGENT_PORT}"
    PORTFOLIO_AGENT_URL = f"http://localhost:{PORTFOLIO_AGENT_PORT}"
    GOALS_AGENT_URL = f"http://localhost:{GOALS_AGENT_PORT}"
    ADVISORS_AGENT_URL = f"http://localhost:{ADVISORS_AGENT_PORT}"
    CHAT_ORCHESTRATOR_URL = f"http://localhost:{CHAT_ORCHESTRATOR_PORT}"
    
    # Gemini Model - using a model that's available for your API key
    MODEL_NAME = "gemini-2.0-flash-exp"
    
    # CORS Configuration
    CORS_ORIGINS = ["*"]
    
    # Mock Banking Data (simplified for demonstration)
    MOCK_USER_ID = "user_123"
    MOCK_SESSION_ID = "session_default"