import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Voice Settings
VOICE_SETTINGS = {
    'voice': 'com.apple.speech.synthesis.voice.samantha',
    'rate': 170,
    'volume': 1.0
}

# Speech Recognition Settings
RECOGNITION_SETTINGS = {
    'energy_threshold': 100,
    'dynamic_energy_threshold': False,
    'pause_threshold': 0.5,
    'operation_timeout': None
}

# OpenAI Settings
OPENAI_SETTINGS = {
    'model': 'gpt-4o-mini',
    'max_tokens': 200,
    'temperature': 0.7
}

# Perplexity Settings
PERPLEXITY_SETTINGS = {
    'model': 'sonar',
    'max_tokens': 200,
    'temperature': 0.3,
    'timeout': 10
}

# Conversation Context Settings
CONTEXT_SETTINGS = {
    'max_context_length': 10,  # Number of previous interactions to remember
    'max_tokens_per_message': 100,  # Max tokens per message in context
    'enable_context': True,  # Enable/disable conversation context
    'context_window': 5  # Number of recent messages to include in context
}

# Autonomous Agent Settings
AUTONOMOUS_SETTINGS = {
    'max_tool_calls': 5,  # Maximum number of tool calls per query
    'enable_autonomous': True,  # Enable autonomous multi-tool execution
    'tool_call_timeout': 30,  # Timeout for tool execution in seconds
    'enable_planning': True,  # Enable planning before tool execution
    'max_planning_steps': 3  # Maximum planning steps
}

# System Prompt
SYSTEM_PROMPT = """You are Jarvis, a witty, efficient AI assistant inspired by Iron Man's AI. 
Respond concisely and helpfully. Use a formal but friendly tone. 

Keep the response very short and concise. Max 15 words.

Available tools and their purposes:
- get_web_data: Search the web for information (web scraping)
- open_any_url: Open a specific website in browser
- open_application: Launch desktop applications
- get_system_stats: Get computer system information
- take_screenshot: Capture screen
- get_current_time: Get current time
- simple_calculator: Perform calculations

Use the appropriate tool for each task:
- For finding information: use get_web_data
- For opening websites: use open_any_url
- For launching apps: use open_application

You can execute multiple tools in sequence if needed to complete a complex task.
Always plan your approach for complex requests and execute tools in the most efficient order.
Maintain conversation context and refer to previous interactions when relevant.
If a request is unsupported, briefly explain what you can help with instead.""" 
