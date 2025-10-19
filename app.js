// Configuration
const ORCHESTRATOR_URL = 'http://localhost:8090';
const APP_NAME = 'chat_orchestrator';
const USER_ID = 'user_123';

// Generate a session ID for this browser session
let sessionId = localStorage.getItem('cymbal_session_id');
if (!sessionId) {
    sessionId = 'session_' + Date.now();
    localStorage.setItem('cymbal_session_id', sessionId);
}

// Message history
let messageHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    addSystemMessage('Welcome to Cymbal Bank! How can I help you with your finances today?');
    
    // Allow Enter to send (Shift+Enter for new line)
    document.getElementById('userInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

function addMessage(text, type) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function addSystemMessage(text) {
    addMessage(text, 'system');
}

function addUserMessage(text) {
    addMessage(text, 'user');
}

function addAgentMessage(text) {
    addMessage(text, 'agent');
}

function addErrorMessage(text) {
    addMessage(text, 'error');
}

function showLoading() {
    const messagesDiv = document.getElementById('messages');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message agent-message loading';
    loadingDiv.id = 'loading-indicator';
    loadingDiv.innerHTML = `
        <div class="loading">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
    `;
    messagesDiv.appendChild(loadingDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function hideLoading() {
    const loadingDiv = document.getElementById('loading-indicator');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

function setQuery(text) {
    document.getElementById('userInput').value = text;
    document.getElementById('userInput').focus();
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    const message = input.value.trim();
    
    if (!message) {
        return;
    }
    
    // Disable input while processing
    input.disabled = true;
    sendButton.disabled = true;
    
    // Add user message to display
    addUserMessage(message);
    
    // Clear input
    input.value = '';
    
    // Show loading indicator
    showLoading();
    
    // Add message to history
    messageHistory.push({
        role: 'user',
        parts: [{ text: message }]
    });
    
    try {
        // Call the agent
        const response = await callAgent(message);
        
        // Hide loading
        hideLoading();
        
        // Add agent response
        addAgentMessage(response);
        
        // Add to history
        messageHistory.push({
            role: 'model',
            parts: [{ text: response }]
        });
        
    } catch (error) {
        hideLoading();
        addErrorMessage('Sorry, I encountered an error. Please make sure all agents are running and try again.');
        console.error('Error:', error);
    } finally {
        // Re-enable input
        input.disabled = false;
        sendButton.disabled = false;
        input.focus();
    }
}

async function callAgent(message) {
    const url = `${ORCHESTRATOR_URL}/run`;
    
    const payload = {
        app_name: APP_NAME,
        user_id: USER_ID,
        session_id: sessionId,
        new_message: {
            role: 'user',
            parts: [{ text: message }]
        },
        streaming: false
    };
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Extract the text response from the ADK response format
        if (data.events && data.events.length > 0) {
            // Find the last event with content
            for (let i = data.events.length - 1; i >= 0; i--) {
                const event = data.events[i];
                if (event.content && event.content.parts) {
                    for (const part of event.content.parts) {
                        if (part.text) {
                            return part.text;
                        }
                    }
                }
            }
        }
        
        // Fallback: if we can't find a proper response
        return 'I received your message but had trouble formatting the response. Please try again.';
        
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Handle connection errors gracefully
window.addEventListener('error', function(e) {
    console.error('Application error:', e);
});