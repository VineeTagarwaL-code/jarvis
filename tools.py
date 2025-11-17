import datetime
import webbrowser
import requests
import platform
import psutil
import os
from config import PERPLEXITY_API_KEY, PERPLEXITY_SETTINGS
from desktop_agent import DesktopAgent

# Initialize desktop agent
desktop_agent = DesktopAgent()

def get_current_time():
    """Get the current system time."""
    return datetime.datetime.now().strftime("%I:%M %p")

def open_any_url(url):
    """Opens any URL in the browser."""
    try:
        webbrowser.open(url)
        return f"Opening {url} in your browser."
    except Exception as e:
        return f"Sorry, I couldn't open {url}. Error: {str(e)}"

def simple_calculator(expression):
    """Evaluate a basic math expression."""
    try:
        # Remove any potentially dangerous characters
        safe_expression = ''.join(c for c in expression if c.isdigit() or c in '+-*/.() ')
        result = eval(safe_expression)
        return f"The result of {expression} is {result}."
    except Exception as e:
        return f"Sorry, I couldn't compute that expression: {expression}"

def get_system_stats():
    """Get comprehensive system specifications and statistics."""
    try:
        stats = []
        
        # OS Information
        stats.append(f"OS: {platform.system()} {platform.release()}")
        stats.append(f"Architecture: {platform.machine()}")
        stats.append(f"Python Version: {platform.python_version()}")
        
        # CPU Information
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        stats.append(f"CPU: {cpu_count} cores, {cpu_percent}% usage")
        
        # Memory Information
        memory = psutil.virtual_memory()
        memory_total = memory.total / (1024**3)  # Convert to GB
        memory_used = memory.used / (1024**3)
        memory_percent = memory.percent
        stats.append(f"Memory: {memory_used:.1f}GB used of {memory_total:.1f}GB ({memory_percent}%)")
        
        # Disk Information
        disk = psutil.disk_usage('/')
        disk_total = disk.total / (1024**3)  # Convert to GB
        disk_used = disk.used / (1024**3)
        disk_free = disk.free / (1024**3)
        disk_percent = (disk.used / disk.total) * 100
        stats.append(f"Disk: {disk_used:.1f}GB used, {disk_free:.1f}GB free of {disk_total:.1f}GB ({disk_percent:.1f}%)")
        
        # Network Information
        network = psutil.net_io_counters()
        bytes_sent = network.bytes_sent / (1024**2)  # Convert to MB
        bytes_recv = network.bytes_recv / (1024**2)
        stats.append(f"Network: {bytes_sent:.1f}MB sent, {bytes_recv:.1f}MB received")
        
        # Boot Time
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.datetime.now() - boot_time
        stats.append(f"Uptime: {uptime.days} days, {uptime.seconds // 3600} hours")
        
        # Process Count
        process_count = len(psutil.pids())
        stats.append(f"Processes: {process_count} running")
        
        return " | ".join(stats)
        
    except Exception as e:
        return f"Sorry, I couldn't retrieve system stats: {str(e)}"

def open_application(app_name, profile_name=None):
    """Open an application by name. For Chrome, optionally specify a profile name."""
    # If it's Chrome and a profile is specified, use the Chrome-specific function
    if "chrome" in app_name.lower() and profile_name:
        return desktop_agent.open_chrome_with_profile(profile_name=profile_name)
    return desktop_agent.open_application(app_name)

def list_chrome_profiles():
    """List all available Chrome profiles."""
    return desktop_agent.list_chrome_profiles()

def open_chrome_with_profile(profile_name=None, profile_id=None):
    """Open Chrome with a specific profile."""
    return desktop_agent.open_chrome_with_profile(profile_name=profile_name, profile_id=profile_id)

def take_screenshot(filename=None):
    """Take a screenshot of the entire screen."""
    return desktop_agent.take_screenshot(filename)

def click_position(x, y):
    """Click at specific coordinates."""
    return desktop_agent.click_position(x, y)

def type_text(text):
    """Type text at current cursor position."""
    return desktop_agent.type_text(text)

def press_key(key):
    """Press a specific key."""
    return desktop_agent.press_key(key)

def get_screen_size():
    """Get screen dimensions."""
    return desktop_agent.get_screen_size()

def get_mouse_position():
    """Get current mouse position."""
    return desktop_agent.get_mouse_position()

def scroll(direction, amount=3):
    """Scroll up or down."""
    return desktop_agent.scroll(direction, amount)

def close_active_window():
    """Close the currently active window."""
    return desktop_agent.close_active_window()

def minimize_window():
    """Minimize the currently active window."""
    return desktop_agent.minimize_window()

def get_running_apps():
    """Get list of currently running applications."""
    return desktop_agent.get_running_apps()

def copy_to_clipboard(text):
    """Copy text to clipboard."""
    return desktop_agent.copy_to_clipboard(text)

def open_system_settings(setting_type="general"):
    """
    Open Windows system settings to a specific page.
    
    Args:
        setting_type: Type of settings (e.g., "display", "text size", "font size", "accessibility", "sound", "network", "privacy", "updates")
    """
    return desktop_agent.open_system_settings(setting_type)

def change_font_size(action="increase", target_percentage=None):
    """
    Change system font/text size on Windows.
    Opens text size settings and attempts to adjust the slider.
    
    Args:
        action: "increase" to make text larger, "decrease" to make it smaller, "set" to set specific percentage, or "open" to just open the settings page
        target_percentage: Target percentage (100-225). Use with action="set" or when user specifies a percentage like "200%"
    """
    return desktop_agent.change_font_size(action, target_percentage)

# Global reference to the current speech handler (set by Jarvis)
_current_speech_handler = None

def _get_speech_handler():
    """Get the current speech handler instance."""
    global _current_speech_handler
    if _current_speech_handler is None:
        from speech_handler import SpeechHandler
        _current_speech_handler = SpeechHandler()
    return _current_speech_handler

def list_voices():
    """List all available TTS voices."""
    handler = _get_speech_handler()
    voices = handler.list_available_voices()
    if not voices:
        return "No voices available."
    
    result = "Available voices:\n"
    for voice in voices:
        result += f"  [{voice['index']}] {voice['name']}\n"
    return result

def set_voice(voice_index=None, voice_name=None):
    """
    Set the TTS voice by index or name.
    
    Args:
        voice_index: Index of the voice (use list_voices to see available indices)
        voice_name: Name of the voice (partial match is supported)
    """
    handler = _get_speech_handler()
    
    if voice_name:
        # Find voice by name (partial match)
        voices = handler.list_available_voices()
        for voice in voices:
            if voice_name.lower() in voice['name'].lower():
                success, message = handler.set_voice(voice_id=voice['id'])
                return message
        return f"Voice not found: {voice_name}. Use list_voices to see available voices."
    elif voice_index is not None:
        success, message = handler.set_voice(voice_index=voice_index)
        return message
    else:
        return "Please provide either voice_index or voice_name. Use list_voices to see available voices."

def get_web_data(query):
    """Fetch real-time web data about a topic or question using Perplexity API."""
    if not PERPLEXITY_API_KEY:
        return "Sorry, I don't have access to web search at the moment."
    
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": PERPLEXITY_SETTINGS['model'],
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Provide only the final answer. Do not include explanations. Provide a list if needed with a short intro."
                },
                {
                    "role": "user", 
                    "content": query
                }
            ],
            "max_tokens": PERPLEXITY_SETTINGS['max_tokens'],
            "temperature": PERPLEXITY_SETTINGS['temperature']
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=data,
            timeout=PERPLEXITY_SETTINGS['timeout']
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"Sorry, I couldn't fetch web data for that query."
            
    except Exception as e:
        return f"Sorry, I encountered an error while searching the web: {str(e)}"

# Function definitions for OpenAI
FUNCTIONS = [
    {
        "name": "get_current_time",
        "description": "Get the current system time.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "open_any_url",
        "description": "Opens any URL in the browser.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "The URL to open"}
            },
            "required": ["url"]
        }
    },
    {
        "name": "simple_calculator",
        "description": "Evaluate a basic math expression.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "The mathematical expression to evaluate"}
            },
            "required": ["expression"]
        }
    },
    {
        "name": "get_system_stats",
        "description": "Get comprehensive system specifications and statistics including OS, CPU, memory, disk, network, and process information.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "open_application",
        "description": "Open a desktop application by name. Supports many common apps including: cursor, whatsapp, terminal, calculator, chrome, edge, firefox, spotify, discord, vscode, code, word, excel, powerpoint, outlook, teams, zoom, slack, steam, obs, photoshop, notepad, cmd, powershell, explorer. For Chrome, you can optionally specify a profile_name to open with a specific profile.",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "The name of the application to open (e.g., 'cursor', 'whatsapp', 'terminal', 'calculator', 'chrome')"},
                "profile_name": {"type": "string", "description": "Optional. For Chrome, specify a profile name to open with (e.g., 'Work', 'Personal', 'Default')"}
            },
            "required": ["app_name"]
        }
    },
    {
        "name": "list_chrome_profiles",
        "description": "List all available Chrome browser profiles. Use this when user asks to see Chrome profiles or wants to select a profile.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "open_chrome_with_profile",
        "description": "Open Google Chrome browser with a specific profile. Use when user asks to open Chrome with a profile or switch Chrome profiles.",
        "parameters": {
            "type": "object",
            "properties": {
                "profile_name": {"type": "string", "description": "Name of the Chrome profile to use (e.g., 'Work', 'Personal', 'Default')"},
                "profile_id": {"type": "string", "description": "Chrome profile ID (use list_chrome_profiles to see IDs)"}
            },
            "required": []
        }
    },
    {
        "name": "take_screenshot",
        "description": "Take a screenshot of the entire screen.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Optional filename for the screenshot"}
            },
            "required": []
        }
    },
    {
        "name": "click_position",
        "description": "Click at specific screen coordinates.",
        "parameters": {
            "type": "object",
            "properties": {
                "x": {"type": "integer", "description": "X coordinate"},
                "y": {"type": "integer", "description": "Y coordinate"}
            },
            "required": ["x", "y"]
        }
    },
    {
        "name": "type_text",
        "description": "Type text at the current cursor position.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to type"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "press_key",
        "description": "Press a specific key (e.g., enter, space, tab, escape, backspace, delete, up, down, left, right).",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The key to press"}
            },
            "required": ["key"]
        }
    },
    {
        "name": "get_screen_size",
        "description": "Get the screen dimensions in pixels.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "get_mouse_position",
        "description": "Get the current mouse cursor position.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "scroll",
        "description": "Scroll up or down on the current page.",
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {"type": "string", "description": "Scroll direction: 'up' or 'down'"},
                "amount": {"type": "integer", "description": "Number of scroll units (default: 3)"}
            },
            "required": ["direction"]
        }
    },
    {
        "name": "close_active_window",
        "description": "Close the currently active window.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "minimize_window",
        "description": "Minimize the currently active window.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "get_running_apps",
        "description": "Get a list of currently running applications.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "copy_to_clipboard",
        "description": "Copy text to the system clipboard.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to copy to clipboard"}
            },
            "required": ["text"]
        }
    },
    {
        "name": "get_web_data",
        "description": "Fetch real-time web data about a topic or question (especially post-2020 events, news, or anything involving today, recent, or this week).",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query or question to search the web for"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "open_system_settings",
        "description": "Open Windows system settings to a specific page. Use this for accessing display settings, accessibility, sound, network, privacy, or update settings.",
        "parameters": {
            "type": "object",
            "properties": {
                "setting_type": {"type": "string", "description": "Type of settings to open: 'display', 'text size', 'font size', 'accessibility', 'sound', 'network', 'privacy', 'updates', or 'general'"}
            },
            "required": ["setting_type"]
        }
    },
    {
        "name": "change_font_size",
        "description": "Change system font/text size on Windows. Opens text size settings and adjusts the slider. Use when user asks to increase, decrease, or set font size to a specific percentage (100-225%). If user specifies a percentage like '200%' or 'to 200%', use action='set' and provide target_percentage. The slider range is 100% to 225%.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {"type": "string", "description": "Action to perform: 'increase' to make text larger, 'decrease' to make it smaller, 'set' to set to a specific percentage, or 'open' to just open the settings page", "enum": ["increase", "decrease", "set", "open"]},
                "target_percentage": {"type": "number", "description": "Target percentage (100-225). Required when action is 'set' or when user specifies a percentage like '200%'"}
            },
            "required": ["action"]
        }
    },
    {
        "name": "list_voices",
        "description": "List all available TTS (text-to-speech) voices. Use when user asks to see available voices or wants to change the voice.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "name": "set_voice",
        "description": "Change the TTS voice used by Jarvis. Use when user asks to change voice, switch voice, or use a different voice. Use list_voices first to see available voices.",
        "parameters": {
            "type": "object",
            "properties": {
                "voice_index": {"type": "integer", "description": "Index of the voice (from list_voices output)"},
                "voice_name": {"type": "string", "description": "Name of the voice (partial match supported, e.g., 'zira', 'david', 'microsoft')"}
            },
            "required": []
        }
    }
]

# Function mapping for easy lookup
FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "open_any_url": open_any_url,
    "simple_calculator": simple_calculator,
    "get_system_stats": get_system_stats,
    "open_application": open_application,
    "take_screenshot": take_screenshot,
    "click_position": click_position,
    "type_text": type_text,
    "press_key": press_key,
    "get_screen_size": get_screen_size,
    "get_mouse_position": get_mouse_position,
    "scroll": scroll,
    "close_active_window": close_active_window,
    "minimize_window": minimize_window,
    "get_running_apps": get_running_apps,
    "copy_to_clipboard": copy_to_clipboard,
    "get_web_data": get_web_data,
    "open_system_settings": open_system_settings,
    "change_font_size": change_font_size,
    "list_voices": list_voices,
    "set_voice": set_voice,
    "list_chrome_profiles": list_chrome_profiles,
    "open_chrome_with_profile": open_chrome_with_profile
} 