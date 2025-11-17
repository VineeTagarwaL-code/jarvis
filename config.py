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
    'pause_threshold': 0.8,  # Increased pause threshold for longer phrases
    'operation_timeout': None
}

# Speech Listening Settings
LISTENING_SETTINGS = {
    'timeout': 20,  # Increased from 10 to 20 seconds
    'phrase_time_limit': 15  # Increased from 6 to 15 seconds for longer commands
}

AUDIO_SETTINGS = {
    'mic_device_index': None,  # None = default, or set to a specific device index
    'auto_select_device': True,  # If True, prompts user to select device on startup
    'tts_delay_after_speak': 0.3,  # Delay in seconds after TTS completes before resuming listening
    'audio_output_device_index': None  # Optional: specify output device index
}

# Browser Settings
BROWSER_SETTINGS = {
    'default_browser': 'chrome',  # 'chrome', 'edge', 'firefox', 'default'
    'chrome_default_profile': None,  # Default Chrome profile name (e.g., 'Work', 'Personal', 'Default')
    'chrome_path': None,  # Auto-detected if None, or specify custom path
    'open_urls_in_new_tab': True,  # Open URLs in new tab vs new window
    'browser_wait_time': 1.0  # Wait time after opening browser (seconds)
}

# Application Paths and Shortcuts
APPLICATION_PATHS = {
    # Custom application paths (leave None for auto-detection)
    'chrome': None,
    'cursor': None,
    'vscode': None,
    'whatsapp': None,
    'discord': None,
    'spotify': None,
    'terminal': None,
    # Add more as needed
}

# Automation Settings
AUTOMATION_SETTINGS = {
    'default_delay': 0.1,  # Default delay between actions (seconds)
    'click_delay': 0.1,  # Delay after clicking (seconds)
    'type_delay': 0.05,  # Delay between keystrokes (seconds)
    'window_switch_delay': 0.5,  # Delay when switching windows (seconds)
    'screenshot_delay': 0.3,  # Delay before taking screenshot (seconds)
    'max_retries': 3,  # Maximum retries for failed operations
    'retry_delay': 1.0,  # Delay between retries (seconds)
    'pyautogui_failsafe': True,  # Enable pyautogui failsafe (move mouse to corner to abort)
    'pyautogui_pause': 0.1  # PyAutoGUI pause between actions
}

# File and Directory Settings
FILE_SETTINGS = {
    'screenshot_directory': None,  # None = current directory, or specify path
    'screenshot_format': 'png',  # 'png', 'jpg', 'jpeg'
    'log_directory': None,  # None = no logging, or specify path for logs
    'temp_directory': None,  # None = system temp, or specify custom temp directory
    'download_directory': None  # Default download directory
}

# System Integration Settings
SYSTEM_INTEGRATION = {
    'enable_system_commands': True,  # Allow system command execution
    'enable_file_operations': True,  # Allow file operations
    'enable_network_operations': True,  # Allow network operations
    'enable_registry_access': False,  # Allow Windows registry access (Windows only)
    'enable_service_control': False,  # Allow Windows service control (Windows only)
    'require_confirmation_for_destructive_actions': True  # Require confirmation for dangerous operations
}

# Performance Settings
PERFORMANCE_SETTINGS = {
    'max_concurrent_operations': 3,  # Maximum concurrent operations
    'operation_timeout': 30,  # Timeout for operations (seconds)
    'cache_enabled': True,  # Enable caching for frequently accessed data
    'cache_ttl': 300,  # Cache time-to-live (seconds)
    'enable_async_operations': False  # Enable async operations (experimental)
}

# UI/UX Settings
UI_SETTINGS = {
    'show_typing_indicator': True,  # Show "Thinking..." indicator
    'show_function_calls': True,  # Show function call notifications
    'show_tool_results': False,  # Show detailed tool execution results
    'response_format': 'concise',  # 'concise', 'detailed', 'verbose'
    'enable_sound_feedback': False,  # Play sound on actions
    'enable_visual_feedback': True  # Show visual feedback
}

# Advanced AI Settings
ADVANCED_AI_SETTINGS = {
    'enable_streaming': False,  # Enable streaming responses (if supported)
    'enable_function_caching': True,  # Cache function results
    'max_function_depth': 5,  # Maximum nested function calls
    'enable_parallel_tool_calls': False,  # Enable parallel tool execution
    'tool_call_retry_on_failure': True,  # Retry failed tool calls
    'enable_smart_retry': True,  # Use AI to determine if retry is needed
    'response_optimization': True  # Optimize responses for speed
}

# Security Settings
SECURITY_SETTINGS = {
    'require_api_key_validation': True,  # Validate API keys on startup
    'sanitize_user_input': True,  # Sanitize user input
    'block_dangerous_commands': True,  # Block potentially dangerous commands
    'allowed_domains': [],  # Whitelist of allowed domains for URL opening (empty = all)
    'blocked_domains': [],  # Blacklist of blocked domains
    'max_url_length': 2048  # Maximum URL length
}

# Notification Settings
NOTIFICATION_SETTINGS = {
    'enable_notifications': False,  # Enable system notifications
    'notification_sound': False,  # Play sound with notifications
    'notification_duration': 5,  # Notification display duration (seconds)
    'show_success_notifications': False,  # Show notifications for successful operations
    'show_error_notifications': True  # Show notifications for errors
}

# Language and Localization
LOCALIZATION_SETTINGS = {
    'language': 'en',  # Language code (en, es, fr, etc.)
    'date_format': '%Y-%m-%d',  # Date format
    'time_format': '%H:%M:%S',  # Time format
    'timezone': None  # None = system timezone, or specify (e.g., 'UTC', 'America/New_York')
}

# Development and Debug Settings
DEBUG_SETTINGS = {
    'debug_mode': False,  # Enable debug mode
    'verbose_logging': False,  # Enable verbose logging
    'log_all_requests': False,  # Log all API requests
    'log_all_responses': False,  # Log all API responses
    'save_conversation_history': False,  # Save conversation history to file
    'conversation_history_path': None  # Path to save conversation history
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

Keep responses short and concise (10-20 words max).

Available tools and their purposes:
- get_web_data: Search the web for real-time information, news, facts, or any query
- open_any_url: Open a specific website URL in the default browser
- open_application: Launch desktop applications by name (e.g., "cursor", "whatsapp", "terminal", "calculator", "chrome", "spotify", "discord", "vscode", "word", "excel", "teams", "zoom"). For Chrome, you can specify a profile_name to open with a specific profile.
- list_chrome_profiles: List all available Chrome browser profiles
- open_chrome_with_profile: Open Chrome with a specific profile (by name or ID)
- get_system_stats: Get computer system information (CPU, memory, disk, etc.)
- take_screenshot: Capture a screenshot of the entire screen
- get_current_time: Get the current system time
- simple_calculator: Perform mathematical calculations
- close_active_window: Close the currently active window
- minimize_window: Minimize the currently active window
- get_running_apps: List currently running applications
- copy_to_clipboard: Copy text to the system clipboard
- open_system_settings: Open Windows system settings (display, accessibility, sound, network, privacy, updates)
- change_font_size: Change system font/text size on Windows (increase, decrease, or set to specific percentage like 200%)
- list_voices: List all available TTS voices
- set_voice: Change the TTS voice used by Jarvis (by index or name)
- click_position: Click at specific screen coordinates (x, y)
- type_text: Type text at the current cursor position
- press_key: Press a specific key (enter, space, tab, escape, etc.)
- scroll: Scroll up or down on the current page
- get_screen_size: Get screen dimensions
- get_mouse_position: Get current mouse cursor position

Tool usage guidelines:
- For finding information or answering questions: use get_web_data
- For opening websites: use open_any_url with the full URL (include https://)
- For launching apps: use open_application with the app name (try common names like "cursor", "whatsapp", "terminal", "calculator")
- For calculations: use simple_calculator with the mathematical expression
- For time queries: use get_current_time
- For system info: use get_system_stats
- For opening Windows Settings: use open_system_settings with setting type (e.g., "display", "font size", "accessibility")
- For changing font size: use change_font_size with action "increase" or "decrease"

When opening applications:
- Use the exact app name the user says (e.g., "cursor" for Cursor IDE, "whatsapp" for WhatsApp, "terminal" for Windows Terminal)
- Common app names: cursor, whatsapp, terminal, calculator, chrome, edge, firefox, spotify, discord, vscode, code, word, excel, powerpoint, outlook, teams, zoom, slack, steam, obs, photoshop
- For Chrome: If user asks to open Chrome with a profile or select a profile, use list_chrome_profiles first to see available profiles, then use open_chrome_with_profile or open_application with profile_name parameter

You can execute multiple tools in sequence if needed to complete a complex task.
Always use the most appropriate tool for each request.
Maintain conversation context and refer to previous interactions when relevant.
If a request is unclear, ask for clarification or make a reasonable assumption based on context.""" 