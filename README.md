# Multi-Agent-Banking-System
Multi-Agent Banking System

A simplified multi-agent AI banking assistant system powered by Google Gemini AI. This system uses specialized AI agents to help users manage their finances across spending, goals, investments, perks, and advisory services.

## Overview

This project implements a multi-agent architecture where an intelligent orchestrator routes user queries to specialized domain expert agents. Each agent focuses on a specific area of personal finance and has access to relevant banking data through a simulated backend.

## Features

- **Intelligent Query Routing**: Chat orchestrator automatically routes questions to the right specialist
- **Spending Analysis**: Track expenses, identify trends, and find savings opportunities
- **Financial Goals**: Set targets, monitor progress, and create savings plans
- **Portfolio Management**: View investments, calculate net worth, and manage debt
- **Banking Perks**: Discover rewards, cashback offers, and maximize benefits
- **Financial Advisors**: Connect with specialists for personalized guidance

## Requirements

- **Python**: 3.10, 3.11, or 3.12
- **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Windows**: Tested on Windows 10/11 (no GPU required)

## Installation

### Step 1: Install Python

Download and install Python 3.10, 3.11, or 3.12 from [python.org](https://www.python.org/downloads/)

Make sure to check "Add Python to PATH" during installation.

### Step 2: Clone or Download the Project

Download all the project files to a directory on your computer.

### Step 3: Install Dependencies

Open Command Prompt or PowerShell in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install all necessary packages including Google ADK, A2A SDK, and Gemini AI libraries.

### Step 4: Configure Your API Key

1. Get your Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Open the `.env` file in a text editor
3. Replace `your_api_key_here` with your actual API key:

```
GOOGLE_API_KEY=AIzaSyB...your_actual_key_here
```

4. Save the file

## Running the System

### Start the Agents

Open Command Prompt or PowerShell in the project directory and run:

```bash
python start_agents.py
```

You should see output indicating that all agents are starting:

```
============================================================
Starting Multi-Agent Banking System
============================================================

Configuration validated successfully!

Starting Spending Agent on port 8081...
Starting Goals Agent on port 8084...
Starting Portfolio Agent on port 8083...
Starting Perks Agent on port 8082...
Starting Advisors Agent on port 8085...
Starting Chat Orchestrator on port 8090...

============================================================
All agents started successfully!
============================================================

Agent URLs:
  Spending Agent:      http://localhost:8081
  Goals Agent:         http://localhost:8084
  Portfolio Agent:     http://localhost:8083
  Perks Agent:         http://localhost:8082
  Advisors Agent:      http://localhost:8085
  Chat Orchestrator:   http://localhost:8090

Open index.html in your browser to start using the system

Press Ctrl+C to stop all agents
============================================================
```

### Open the Web Interface

1. Open the `index.html` file in your web browser (Chrome, Firefox, Edge, etc.)
2. You should see the Cymbal Bank interface
3. Start chatting with the AI banking assistant!

## Usage Examples

Try these example queries:

### Spending Analysis
- "What did I spend on groceries last month?"
- "Show me my spending by category"
- "How can I reduce my monthly expenses?"
- "What are my biggest spending categories?"

### Financial Goals
- "How am I doing on my emergency fund goal?"
- "I want to save $5,000 for a vacation in 8 months. How much should I save monthly?"
- "Show me progress on all my goals"
- "What's my Italy trip savings goal status?"

### Portfolio & Investments
- "What is my net worth?"
- "Show me my investment portfolio"
- "What's the best way to pay off my debts?"
- "How should I prioritize my loan payments?"

### Banking Perks
- "What perks can save me money?"
- "Show me my active cashback rewards"
- "What benefits am I eligible for?"
- "Calculate my total potential savings from perks"

### Financial Advisors
- "I need help with retirement planning"
- "Find me an advisor for debt management"
- "Who are the available financial advisors?"
- "I want to talk to someone about investments"

## How It Works

### Architecture

The system consists of six independent Python agents:

1. **Chat Orchestrator** (Port 8090): Routes queries to appropriate specialists
2. **Spending Agent** (Port 8081): Handles spending and transaction queries
3. **Goals Agent** (Port 8084): Manages financial goals and savings plans
4. **Portfolio Agent** (Port 8083): Deals with investments and debt
5. **Perks Agent** (Port 8082): Manages rewards and benefits
6. **Advisors Agent** (Port 8085): Connects users with financial advisors

### Data Flow

1. User types a question in the web interface
2. Frontend sends the question to the Chat Orchestrator
3. Orchestrator analyzes the query and routes it to the appropriate specialist agent
4. Specialist agent uses its tools to access relevant banking data
5. Agent generates a response using Gemini AI
6. Response is sent back through the orchestrator to the user

### Mock Data

The system uses simulated banking data for demonstration purposes. In a production environment, these would connect to real banking APIs. The mock data includes:

- 90 days of transaction history
- Financial goals and savings targets
- Investment portfolio with performance data
- Debt information (credit cards, loans)
- Banking perks and rewards
- Financial advisor profiles

## Troubleshooting

### Problem: "GOOGLE_API_KEY environment variable not set"

**Solution**: Make sure