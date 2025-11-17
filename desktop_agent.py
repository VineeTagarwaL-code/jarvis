import subprocess
import os
import platform
import pyautogui
import time
import json
from PIL import Image
import psutil

class DesktopAgent:
    def __init__(self):
        self.system = platform.system()
        # Set pyautogui safety settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def open_application(self, app_name):
        """Open an application by name."""
        try:
            if self.system == "Darwin":  # macOS
                # Common macOS apps
                app_mapping = {
                    "chrome": "Google Chrome",
                    "safari": "Safari",
                    "firefox": "Firefox",
                    "spotify": "Spotify",
                    "terminal": "Terminal",
                    "finder": "Finder",
                    "mail": "Mail",
                    "messages": "Messages",
                    "facetime": "FaceTime",
                    "photos": "Photos",
                    "music": "Music",
                    "calculator": "Calculator",
                    "notes": "Notes",
                    "calendar": "Calendar",
                    "reminders": "Reminders",
                    "maps": "Maps",
                    "weather": "Weather",
                    "clock": "Clock",
                    "settings": "System Preferences",
                    "preferences": "System Preferences"
                }
                
                app_name_lower = app_name.lower()
                actual_app_name = app_mapping.get(app_name_lower, app_name)
                
                subprocess.run(["open", "-a", actual_app_name])
                return f"Opened {actual_app_name}"
                
            elif self.system == "Windows":
                # Windows Settings and System Apps (use ms-settings: URI)
                settings_mapping = {
                    "settings": "ms-settings:",
                    "windows settings": "ms-settings:",
                    "system settings": "ms-settings:",
                    "display settings": "ms-settings:display",
                    "accessibility": "ms-settings:easeofaccess",
                    "text size": "ms-settings:easeofaccess-display",
                    "font size": "ms-settings:easeofaccess-display",
                    "sound settings": "ms-settings:sound",
                    "network settings": "ms-settings:network",
                    "privacy settings": "ms-settings:privacy",
                    "update settings": "ms-settings:windowsupdate"
                }
                
                app_name_lower = app_name.lower().strip()
                
                # Check if it's a settings URI
                if app_name_lower in settings_mapping:
                    try:
                        subprocess.Popen(f'start {settings_mapping[app_name_lower]}', shell=True)
                        return f"Opened {app_name}"
                    except Exception as e:
                        return f"Could not open {app_name}: {str(e)}"
                
                # Common Windows apps with multiple aliases
                app_mapping = {
                    "chrome": "chrome.exe",
                    "google chrome": "chrome.exe",
                    "chrome browser": "chrome.exe",
                    "browser": "chrome.exe",  # Default to Chrome
                    "edge": "msedge.exe",
                    "microsoft edge": "msedge.exe",
                    "firefox": "firefox.exe",
                    "mozilla firefox": "firefox.exe",
                    "notepad": "notepad.exe",
                    "calculator": "calc.exe",
                    "calc": "calc.exe",
                    "explorer": "explorer.exe",
                    "file explorer": "explorer.exe",
                    "cmd": "cmd.exe",
                    "command prompt": "cmd.exe",
                    "powershell": "powershell.exe",
                    "terminal": "wt.exe",  # Windows Terminal
                    "windows terminal": "wt.exe",
                    "cursor": "Cursor.exe",  # Cursor IDE
                    "whatsapp": "WhatsApp.exe",
                    "discord": "Discord.exe",
                    "spotify": "Spotify.exe",
                    "vscode": "Code.exe",
                    "visual studio code": "Code.exe",
                    "code": "Code.exe",
                    "steam": "steam.exe",
                    "obs": "obs64.exe",
                    "obs studio": "obs64.exe",
                    "vlc": "vlc.exe",
                    "photoshop": "Photoshop.exe",
                    "illustrator": "Illustrator.exe",
                    "premiere": "Adobe Premiere Pro.exe",
                    "excel": "EXCEL.EXE",
                    "word": "WINWORD.EXE",
                    "powerpoint": "POWERPNT.EXE",
                    "outlook": "OUTLOOK.EXE",
                    "teams": "Teams.exe",
                    "zoom": "Zoom.exe",
                    "slack": "slack.exe"
                }
                
                actual_app_name = app_mapping.get(app_name_lower, None)
                
                # Try direct mapping first
                if actual_app_name:
                    try:
                        # For Chrome, try multiple methods
                        if "chrome" in app_name_lower:
                            return self._open_chrome()
                        else:
                            subprocess.Popen(actual_app_name, shell=True)
                            return f"Opened {app_name}"
                    except Exception:
                        pass
                
                # Try Windows Start Menu search using shell:AppsFolder
                try:
                    # Use 'start' command to search Windows Start Menu
                    # This works better for UWP apps and installed programs
                    subprocess.Popen(f'start "" "{app_name}"', shell=True)
                    time.sleep(0.5)  # Give it a moment to launch
                    return f"Opened {app_name}"
                except Exception:
                    pass
                
                # Try using shell:AppsFolder for UWP apps
                try:
                    subprocess.Popen(f'explorer shell:AppsFolder\\{app_name}', shell=True)
                    time.sleep(0.5)
                    return f"Opened {app_name}"
                except Exception:
                    pass
                
                # Try common installation paths (limited depth for performance)
                common_paths = [
                    (os.path.expanduser("~\\AppData\\Local\\Programs"), 2),  # (path, max_depth)
                    (os.path.expanduser("~\\AppData\\Local"), 1),
                ]
                
                # Search for the app in common paths
                app_name_variants = [
                    app_name + ".exe",
                    app_name.capitalize() + ".exe",
                    app_name.title().replace(" ", "") + ".exe"
                ]
                
                def search_path(path, max_depth, current_depth=0):
                    """Recursively search path with depth limit."""
                    if current_depth > max_depth:
                        return None
                    try:
                        for item in os.listdir(path):
                            item_path = os.path.join(path, item)
                            if os.path.isfile(item_path):
                                for variant in app_name_variants:
                                    if item.lower() == variant.lower():
                                        return item_path
                            elif os.path.isdir(item_path) and current_depth < max_depth:
                                result = search_path(item_path, max_depth, current_depth + 1)
                                if result:
                                    return result
                    except (PermissionError, OSError):
                        pass
                    return None
                
                for path, max_depth in common_paths:
                    if os.path.exists(path):
                        result = search_path(path, max_depth)
                        if result:
                            try:
                                subprocess.Popen(result)
                                return f"Opened {app_name}"
                            except Exception:
                                continue
                
                return f"Could not find or open {app_name}. Please check if it's installed."
                
            elif self.system == "Linux":
                # Common Linux apps
                app_mapping = {
                    "chrome": "google-chrome",
                    "firefox": "firefox",
                    "terminal": "gnome-terminal",
                    "calculator": "gnome-calculator",
                    "files": "nautilus",
                    "gedit": "gedit"
                }
                
                app_name_lower = app_name.lower()
                actual_app_name = app_mapping.get(app_name_lower, app_name)
                
                subprocess.Popen([actual_app_name])
                return f"Opened {actual_app_name}"
                
        except Exception as e:
            return f"Could not open {app_name}: {str(e)}"
    
    def take_screenshot(self, filename=None):
        """Take a screenshot of the entire screen."""
        try:
            if filename is None:
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            return f"Could not take screenshot: {str(e)}"
    
    def click_position(self, x, y):
        """Click at specific coordinates."""
        try:
            pyautogui.click(x, y)
            return f"Clicked at position ({x}, {y})"
        except Exception as e:
            return f"Could not click at position ({x}, {y}): {str(e)}"
    
    def type_text(self, text):
        """Type text at current cursor position."""
        try:
            pyautogui.typewrite(text)
            return f"Typed: {text}"
        except Exception as e:
            return f"Could not type text: {str(e)}"
    
    def press_key(self, key):
        """Press a specific key."""
        try:
            pyautogui.press(key)
            return f"Pressed key: {key}"
        except Exception as e:
            return f"Could not press key {key}: {str(e)}"
    
    def get_screen_size(self):
        """Get screen dimensions."""
        try:
            width, height = pyautogui.size()
            return f"Screen size: {width}x{height} pixels"
        except Exception as e:
            return f"Could not get screen size: {str(e)}"
    
    def get_mouse_position(self):
        """Get current mouse position."""
        try:
            x, y = pyautogui.position()
            return f"Mouse position: ({x}, {y})"
        except Exception as e:
            return f"Could not get mouse position: {str(e)}"
    
    def scroll(self, direction, amount=3):
        """Scroll up or down."""
        try:
            if direction.lower() in ["up", "scrollup"]:
                pyautogui.scroll(amount)
                return f"Scrolled up {amount} units"
            elif direction.lower() in ["down", "scrolldown"]:
                pyautogui.scroll(-amount)
                return f"Scrolled down {amount} units"
            else:
                return "Invalid scroll direction. Use 'up' or 'down'"
        except Exception as e:
            return f"Could not scroll: {str(e)}"
    
    def close_active_window(self):
        """Close the currently active window."""
        try:
            if self.system == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'w')
            elif self.system == "Windows":
                pyautogui.hotkey('alt', 'f4')
            elif self.system == "Linux":
                pyautogui.hotkey('ctrl', 'w')
            return "Closed active window"
        except Exception as e:
            return f"Could not close window: {str(e)}"
    
    def minimize_window(self):
        """Minimize the currently active window."""
        try:
            if self.system == "Darwin":  # macOS
                pyautogui.hotkey('cmd', 'm')
            elif self.system == "Windows":
                pyautogui.hotkey('win', 'down')
            elif self.system == "Linux":
                pyautogui.hotkey('ctrl', 'super', 'down')
            return "Minimized active window"
        except Exception as e:
            return f"Could not minimize window: {str(e)}"
    
    def get_running_apps(self):
        """Get list of currently running applications."""
        try:
            running_apps = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    running_apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Get unique apps and limit to top 10
            unique_apps = list(set(running_apps))[:10]
            return f"Running apps: {', '.join(unique_apps)}"
        except Exception as e:
            return f"Could not get running apps: {str(e)}"
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        try:
            import pyperclip
            pyperclip.copy(text)
            return f"Copied '{text}' to clipboard"
        except ImportError:
            # Fallback method using pyautogui
            try:
                pyautogui.write(text)
                if self.system == "Darwin":  # macOS
                    pyautogui.hotkey('cmd', 'a')  # Select all
                    pyautogui.hotkey('cmd', 'c')  # Copy
                elif self.system == "Windows":
                    pyautogui.hotkey('ctrl', 'a')  # Select all
                    pyautogui.hotkey('ctrl', 'c')  # Copy
                elif self.system == "Linux":
                    pyautogui.hotkey('ctrl', 'a')  # Select all
                    pyautogui.hotkey('ctrl', 'c')  # Copy
                return f"Copied '{text}' to clipboard"
            except Exception as e:
                return f"Could not copy to clipboard: {str(e)}"
        except Exception as e:
            return f"Could not copy to clipboard: {str(e)}"
    
    def open_system_settings(self, setting_type="general"):
        """
        Open Windows system settings to a specific page.
        
        Args:
            setting_type: Type of settings to open. Options:
                - "general", "settings", "system": General settings
                - "display", "text size", "font size": Display/Text size settings
                - "accessibility": Accessibility settings
                - "sound": Sound settings
                - "network": Network settings
                - "privacy": Privacy settings
                - "updates": Windows Update settings
        """
        if self.system != "Windows":
            return "System settings access is currently only supported on Windows."
        
        settings_uris = {
            "general": "ms-settings:",
            "settings": "ms-settings:",
            "system": "ms-settings:",
            "display": "ms-settings:display",
            "text size": "ms-settings:easeofaccess-display",
            "font size": "ms-settings:easeofaccess-display",
            "accessibility": "ms-settings:easeofaccess",
            "sound": "ms-settings:sound",
            "network": "ms-settings:network",
            "privacy": "ms-settings:privacy",
            "updates": "ms-settings:windowsupdate"
        }
        
        setting_type_lower = setting_type.lower()
        uri = settings_uris.get(setting_type_lower, "ms-settings:")
        
        try:
            subprocess.Popen(f'start {uri}', shell=True)
            return f"Opened {setting_type} settings"
        except Exception as e:
            return f"Could not open {setting_type} settings: {str(e)}"
    
    def change_font_size(self, action="increase", target_percentage=None):
        """
        Change system font/text size on Windows.
        Opens the text size settings page where user can adjust the slider.
        
        Args:
            action: "increase", "decrease", "set", or "open" to just open settings
            target_percentage: Target percentage (100-225). If provided, calculates exact number of presses needed.
        """
        if self.system != "Windows":
            return "Font size changes are currently only supported on Windows."
        
        try:
            # Open the text size settings page
            subprocess.Popen('start ms-settings:easeofaccess-display', shell=True)
            time.sleep(1.5)  # Wait for settings to open
            
            # Windows text size slider: 100% (leftmost) to 225% (rightmost)
            # Each arrow key press moves approximately 3-4% (roughly 3.125% per press for 125% range / 40 steps)
            MIN_PERCENTAGE = 100
            MAX_PERCENTAGE = 225
            PERCENTAGE_PER_PRESS = 3.125  # Approximately 3.125% per press (125% range / 40 steps)
            
            if target_percentage is not None:
                # Set to specific percentage
                try:
                    target = float(target_percentage)
                    # Clamp to valid range
                    target = max(MIN_PERCENTAGE, min(MAX_PERCENTAGE, target))
                    
                    # Calculate number of presses needed from 100% (default/leftmost position)
                    # We'll move to the leftmost first, then right to target
                    presses_needed = int((target - MIN_PERCENTAGE) / PERCENTAGE_PER_PRESS)
                    
                    # Move to leftmost position first (reset)
                    pyautogui.press('left', presses=50)  # Move all the way left
                    time.sleep(0.3)
                    
                    # Then move to target
                    pyautogui.press('right', presses=presses_needed)
                    return f"Set font size to {target:.0f}%"
                except (ValueError, TypeError):
                    return f"Invalid target percentage. Please use a number between {MIN_PERCENTAGE} and {MAX_PERCENTAGE}."
            
            elif action.lower() == "increase":
                # Try to increase font size using keyboard
                # The slider is usually focused, so we can use arrow keys
                pyautogui.press('right', presses=3)  # Move slider right (increase)
                return "Increased font size. You can adjust further in the settings window."
            elif action.lower() == "decrease":
                # Try to decrease font size
                pyautogui.press('left', presses=3)  # Move slider left (decrease)
                return "Decreased font size. You can adjust further in the settings window."
            elif action.lower() == "set":
                return "Please specify a target percentage (100-225)."
            else:
                return "Opened text size settings. Use the slider to adjust font size."
        except Exception as e:
            return f"Opened text size settings. Error adjusting slider: {str(e)}. Please adjust manually."
    
    def _find_chrome_path(self):
        """Find Chrome executable path."""
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
        ]
        for path in chrome_paths:
            if os.path.exists(path):
                return path
        return None
    
    def _get_chrome_profiles(self):
        """Get list of Chrome profiles."""
        try:
            local_app_data = os.getenv('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local'))
            chrome_user_data = os.path.join(local_app_data, 'Google', 'Chrome', 'User Data')
            preferences_path = os.path.join(chrome_user_data, 'Local State')
            
            if not os.path.exists(preferences_path):
                return []
            
            with open(preferences_path, 'r', encoding='utf-8') as f:
                local_state = json.load(f)
            
            profiles = []
            profile_info = local_state.get('profile', {}).get('info_cache', {})
            
            for profile_id, profile_data in profile_info.items():
                profiles.append({
                    'id': profile_id,
                    'name': profile_data.get('name', 'Default'),
                    'email': profile_data.get('user_name', '')
                })
            
            return profiles
        except Exception as e:
            print(f"Error reading Chrome profiles: {e}")
            return []
    
    def _open_chrome(self, profile_name=None, profile_id=None):
        """Open Chrome with optional profile selection."""
        from config import BROWSER_SETTINGS
        
        chrome_path = self._find_chrome_path()
        if not chrome_path:
            # Try Start Menu search
            try:
                subprocess.Popen('start "" "Google Chrome"', shell=True)
                time.sleep(0.5)
                return "Opened Chrome"
            except:
                pass
            # Fallback
            subprocess.Popen("chrome.exe", shell=True)
            return "Opened Chrome"
        
        # Get default profile from config if not specified
        if not profile_name and not profile_id:
            profile_name = BROWSER_SETTINGS.get('chrome_default_profile')
        
        # Build Chrome command
        cmd = [chrome_path]
        
        if profile_name or profile_id:
            profiles = self._get_chrome_profiles()
            target_profile_id = None
            
            if profile_id:
                target_profile_id = profile_id
            elif profile_name:
                # Find profile by name
                for profile in profiles:
                    if profile_name.lower() in profile['name'].lower():
                        target_profile_id = profile['id']
                        break
            
            if target_profile_id:
                cmd.append(f'--profile-directory={target_profile_id}')
            else:
                # If profile not found, open Chrome normally and let user select
                subprocess.Popen(chrome_path)
                time.sleep(1)
                # Try to open profile picker
                pyautogui.hotkey('ctrl', 'shift', 'm')  # Chrome profile switcher shortcut
                return f"Opened Chrome. Profile picker should appear. Requested profile: {profile_name or 'default'}"
        else:
            # Open with default profile
            subprocess.Popen(chrome_path)
            return "Opened Chrome"
        
        subprocess.Popen(cmd)
        profile_display = profile_name or profile_id or "default"
        return f"Opened Chrome with profile: {profile_display}"
    
    def list_chrome_profiles(self):
        """List all available Chrome profiles."""
        profiles = self._get_chrome_profiles()
        if not profiles:
            return "No Chrome profiles found."
        
        result = "Available Chrome profiles:\n"
        for i, profile in enumerate(profiles):
            email_info = f" ({profile['email']})" if profile['email'] else ""
            result += f"  [{i}] {profile['name']}{email_info}\n"
        return result
    
    def open_chrome_with_profile(self, profile_name=None, profile_id=None):
        """Open Chrome with a specific profile."""
        return self._open_chrome(profile_name=profile_name, profile_id=profile_id) 