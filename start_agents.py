import subprocess
import sys
import time
from pathlib import Path
from config import Config

def start_agent(agent_module, port, name):
    """Start a single agent server"""
    print(f"Starting {name} on port {port}...")
    
    # Use subprocess to start the agent in the background
    cmd = [
        sys.executable, "-m", "google.adk.cli.server",
        agent_module,
        "--port", str(port),
        "--allow_origins", "*"
    ]
    
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process

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
        print("See .env.template for an example")
        return
    
    # Check for API key
    if not Config.GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY not set in .env file!")
        print("Please add your Google API key to the .env file")
        return
    
    print("Configuration validated successfully!")
    print()
    
    # Agent configurations
    agents = [
        ("spending_agent:spending_agent", Config.SPENDING_AGENT_PORT, "Spending Agent"),
        ("goals_agent:goals_agent", Config.GOALS_AGENT_PORT, "Goals Agent"),
        ("portfolio_agent:portfolio_agent", Config.PORTFOLIO_AGENT_PORT, "Portfolio Agent"),
        ("perks_agent:perks_agent", Config.PERKS_AGENT_PORT, "Perks Agent"),
        ("advisors_agent:advisors_agent", Config.ADVISORS_AGENT_PORT, "Advisors Agent"),
        ("main_orchestrator:root_agent", Config.CHAT_ORCHESTRATOR_PORT, "Chat Orchestrator"),
    ]
    
    # Start all agents
    processes = []
    for agent_module, port, name in agents:
        try:
            process = start_agent(agent_module, port, name)
            processes.append((process, name, port))
            time.sleep(2)  # Give each agent time to start
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
        # Wait for all processes
        while True:
            time.sleep(1)
            # Check if any process has died
            for process, name, port in processes:
                if process.poll() is not None:
                    print(f"\nWARNING: {name} (port {port}) has stopped!")
    except KeyboardInterrupt:
        print("\n\nStopping all agents...")
        for process, name, port in processes:
            process.terminate()
            print(f"Stopped {name}")
        print("\nAll agents stopped successfully!")

if __name__ == "__main__":
    main()