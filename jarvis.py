from speech_handler import SpeechHandler
from ai_handler import AIHandler
from config import OPENAI_API_KEY, PERPLEXITY_API_KEY
from speak import speak
class Jarvis:
    def __init__(self):
        self.speech_handler = SpeechHandler()
        self.ai_handler = AIHandler()
        self.is_running = False
    
    def start(self):
        """Start Jarvis and begin listening for commands."""
        print("Jarvis is starting up...")
        print(f"OpenAI API Key loaded: {'Yes' if OPENAI_API_KEY else 'No'}")
        print(f"Perplexity API Key loaded: {'Yes' if PERPLEXITY_API_KEY else 'No'}")
        
        # Calibrate microphone
        self.speech_handler.calibrate_microphone()
        
        self.is_running = True
        self._main_loop()
    
    def stop(self):
        """Stop Jarvis."""
        self.is_running = False
        speak("Shutting down Jarvis. Goodbye!")
        print("Jarvis has been shut down.")
    
    def _main_loop(self):
        """Main loop for processing user input."""
        while self.is_running:
            # Listen for speech
            text = self.speech_handler.listen_for_speech()
            
            if text is None:
                continue
            
            # Check for stop command
            if text.lower() == "stop":
                self.stop()
                break
            
            # Check for conversation management commands
            if text.lower() == "clear history":
                response = self.ai_handler.clear_conversation_history()
                print(f"Jarvis: {response}")
                speak(response)
                continue
            
            if text.lower() == "conversation stats":
                stats = self.ai_handler.get_conversation_stats()
                response = f"Conversation stats: {stats['total_interactions']} interactions, {stats['total_tool_calls']} tool calls, average {stats['average_tools_per_interaction']:.1f} tools per interaction."
                print(f"Jarvis: {response}")
                speak(response)
                continue
            
            # Process query if it contains "jarvis"
            query = text.lower().replace("jarvis", "").strip()
            if query:
                    # Get response from AI
                    response = self.ai_handler.process_query(query)
                    
                    # Speak the response
                    print(f"Jarvis: {response}")
                    speak(response)
            else:
                speak("Yes, sir? How can I help you?")
    
    def process_text_command(self, text):
        """Process a text command (useful for testing or alternative input methods)."""
        if "jarvis" in text.lower():
            query = text.lower().replace("jarvis", "").strip()
            if query:
                response = self.ai_handler.process_query(query)
                print(f"Jarvis: {response}")
                return response
        return None
    
    def get_conversation_stats(self):
        """Get conversation statistics."""
        return self.ai_handler.get_conversation_stats()
    
    def clear_history(self):
        """Clear conversation history."""
        return self.ai_handler.clear_conversation_history() 
