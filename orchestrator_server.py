
from main_orchestrator import root_agent
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
    """Run the agent and return response"""
    try:
        user_message = request.new_message.parts[0].text
        
        # Process with the agent
        response_text = root_agent.process_query(user_message)
        
        # Format response
        events = [
            {
                "content": {
                    "parts": [
                        {"text": response_text}
                    ]
                },
                "role": "model"
            }
        ]
        
        return RunResponse(events=events)
    except Exception as e:
        return RunResponse(events=[{
            "content": {"parts": [{"text": f"Error: {str(e)}"}]},
            "role": "model"
        }])

@app.get("/health")
async def health():
    return {"status": "ok"}
