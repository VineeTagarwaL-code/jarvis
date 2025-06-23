#!/usr/bin/env python3
"""
Jarvis - AI Voice Assistant
A modular voice assistant with speech recognition, AI processing, and function calling.
"""

from jarvis import Jarvis
from speak import speak
def main():
    """Main entry point for the Jarvis application."""
    try:
        # Create and start Jarvis
        speak("Hello, how can I help you today?, My name is Jarvis and I am your personal assistant, I am here to help you with your tasks and questions")
        jarvis = Jarvis()
        jarvis.start()
    except KeyboardInterrupt:
        print("\nJarvis interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
