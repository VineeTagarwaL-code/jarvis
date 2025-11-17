#!/usr/bin/env python3
"""
Jarvis - AI Voice Assistant
A modular voice assistant with speech recognition, AI processing, and function calling.
"""

from jarvis import Jarvis
from speech_handler import SpeechHandler
from config import AUDIO_SETTINGS

def select_audio_device():
    """
    Display available audio devices and allow user to select a microphone.
    
    Returns:
        int or None: Selected microphone device index, or None for default
    """
    # Get unique devices (deduplicated)
    devices = SpeechHandler.list_unique_audio_devices()
    
    if not devices:
        print("No input devices found. Using default microphone.")
        return None
    
    # Display devices
    SpeechHandler.print_audio_devices()
    
    # Get valid device indices for validation message
    device_indices = [d['index'] for d in devices]
    min_idx = min(device_indices)
    max_idx = max(device_indices)
    
    print("Select a microphone device:")
    print("  [Enter] - Use default microphone")
    if len(device_indices) > 1:
        print(f"  [{min_idx}-{max_idx}] - Select a specific device")
    else:
        print(f"  [{min_idx}] - Select this device")
    
    while True:
        try:
            user_input = input("\nEnter device number (or press Enter for default): ").strip()
            
            # If empty, use default
            if not user_input:
                print("Using default microphone.")
                return None
            
            # Try to parse as integer
            device_index = int(user_input)
            
            # Validate device index
            if device_index in device_indices:
                selected_device = next(d for d in devices if d['index'] == device_index)
                print(f"Selected: {selected_device['name']}")
                return device_index
            else:
                valid_indices_str = ", ".join(map(str, sorted(device_indices)))
                print(f"Invalid device number. Valid options: {valid_indices_str} (or press Enter for default)")
        
        except ValueError:
            print("Invalid input. Please enter a number or press Enter for default.")
        except KeyboardInterrupt:
            print("\nUsing default microphone.")
            return None

def main():
    """Main entry point for the Jarvis application."""
    try:
        # Get microphone device index from config or user selection
        mic_device_index = None
        
        if AUDIO_SETTINGS['auto_select_device']:
            # Prompt user to select device
            mic_device_index = select_audio_device()
        else:
            # Use device from config
            mic_device_index = AUDIO_SETTINGS['mic_device_index']
            if mic_device_index is not None:
                print(f"Using configured microphone device index: {mic_device_index}")
            else:
                print("Using default microphone device.")
        
        # Create and start Jarvis with selected device
        jarvis = Jarvis(mic_device_index=mic_device_index)
        jarvis.start()
    except KeyboardInterrupt:
        print("\nJarvis interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()