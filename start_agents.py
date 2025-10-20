import subprocess
import sys
import time
from pathlib import Path
from config import Config

def start_agent_server(agent_file, agent_name, port):
    """Start an ADK agent server"""
    print(f"Starting {agent_name} on port {port}...")
    
    # Use ADK's built-in server command
    cmd = [
        sys.executable, "-m", "uvicorn",
        f"{agent_file}:app",
        "--host", "0.0.0.0",
        "--port", str(port),
        "--log-level", "error"
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
    )
    
    return process

def create_app_file(agent_module, agent_var, output_file):
    """Create a simple app file that uvicorn can run"""
    app_content = f"""
from {agent_module} import {agent_var}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessagePart(BaseModel):
    text: str

class Message(BaseModel):
    role: str
    parts: List[MessagePart]

class RunRequest(BaseModel):
    app_name: str
    user_id: str
    session_id: str
    new_message: Message
    streaming: bool = False

class RunResponse(BaseModel):
    events: List[Dict[str, Any]]

@app.post("/run", response_model=RunResponse)
async def run_agent(request: RunRequest):
    \"\"\"Run the agent and return response\"\"\"
    try:
        user_message = request.new_message.parts[0].text
        
        # Process with the agent
        response_text = {agent_var}.process_query(user_message)
        
        # Format response
        events = [
            {{
                "content": {{
                    "parts": [
                        {{"text": response_text}}
                    ]
                }},
                "role": "model"
            }}
        ]
        
        return RunResponse(events=events)
    except Exception as e:
        return RunResponse(events=[{{
            "content": {{"parts": [{{"text": f"Error: {{str(e)}}"}}]}},
            "role": "model"
        }}])

@app.get("/health")
async def health():
    return {{"status": "ok"}}
"""
    
    with open(output_file, 'w') as f:
        f.write(app_content)

def main():
    """Start all agents"""
    print("=" * 60)
    print("Starting Multi-Agent Banking System")
    print("=" * 60)
    print()
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("ERROR: .env file not found!")
        print("Please create a .env file with your GOOGLE_API_KEY")
        return
    
    # Check for API key
    if not Config.GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY not set in .env file!")
        return
    
    print("Configuration validated successfully!")
    print()
    
    # Create app files for each agent
    print("Creating agent server files...")
    
    agents_config = [
        ("spending_agent", "spending_agent", "spending_server.py", Config.SPENDING_AGENT_PORT, "Spending Agent"),
        ("goals_agent", "goals_agent", "goals_server.py", Config.GOALS_AGENT_PORT, "Goals Agent"),
        ("portfolio_agent", "portfolio_agent", "portfolio_server.py", Config.PORTFOLIO_AGENT_PORT, "Portfolio Agent"),
        ("perks_agent", "perks_agent", "perks_server.py", Config.PERKS_AGENT_PORT, "Perks Agent"),
        ("advisors_agent", "advisors_agent", "advisors_server.py", Config.ADVISORS_AGENT_PORT, "Advisors Agent"),
        ("main_orchestrator", "root_agent", "orchestrator_server.py", Config.CHAT_ORCHESTRATOR_PORT, "Chat Orchestrator"),
    ]
    
    # Create server files
    for module, var, server_file, port, name in agents_config:
        create_app_file(module, var, server_file)
    
    print("Server files created successfully!")
    print()
    
    # Start all agents
    processes = []
    for module, var, server_file, port, name in agents_config:
        try:
            # Remove .py extension for module name
            server_module = server_file.replace('.py', '')
            process = start_agent_server(server_module, name, port)
            processes.append((process, name, port))
            time.sleep(3)  # Give each agent more time to start
        except Exception as e:
            print(f"ERROR starting {name}: {e}")
            return
    
    print()
    print("=" * 60)
    print("All agents started successfully!")
    print("=" * 60)
    print()
    print("Agent URLs:")
    print(f"  Spending Agent:      {Config.SPENDING_AGENT_URL}")
    print(f"  Goals Agent:         {Config.GOALS_AGENT_URL}")
    print(f"  Portfolio Agent:     {Config.PORTFOLIO_AGENT_URL}")
    print(f"  Perks Agent:         {Config.PERKS_AGENT_URL}")
    print(f"  Advisors Agent:      {Config.ADVISORS_AGENT_URL}")
    print(f"  Chat Orchestrator:   {Config.CHAT_ORCHESTRATOR_URL}")
    print()
    print("Open index.html in your browser to start using the system")
    print()
    print("Press Ctrl+C to stop all agents")
    print("=" * 60)
    
    try:
        # Wait for processes
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping all agents...")
        for process, name, port in processes:
            process.terminate()
            print(f"Stopped {name}")
        print("\nAll agents stopped successfully!")

if __name__ == "__main__":
    main()