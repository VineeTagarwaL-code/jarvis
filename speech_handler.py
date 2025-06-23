import speech_recognition as sr
import pyttsx3
from config import VOICE_SETTINGS, RECOGNITION_SETTINGS

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.mic = sr.Microphone()
        
        # Configure voice settings
        self.engine.setProperty('voice', VOICE_SETTINGS['voice'])
        self.engine.setProperty('rate', VOICE_SETTINGS['rate'])
        self.engine.setProperty('volume', VOICE_SETTINGS['volume'])
        
        # Configure recognition settings
        self.recognizer.energy_threshold = RECOGNITION_SETTINGS['energy_threshold']
        self.recognizer.dynamic_energy_threshold = RECOGNITION_SETTINGS['dynamic_energy_threshold']
        self.recognizer.pause_threshold = RECOGNITION_SETTINGS['pause_threshold']
        self.recognizer.operation_timeout = RECOGNITION_SETTINGS['operation_timeout']
    
    def calibrate_microphone(self, duration=0.5):
        """Calibrate microphone for ambient noise."""
        print("Calibrating microphone for ambient noise...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)
        print("Calibration complete. Jarvis is ready!")
    
    def listen_for_speech(self, timeout=10, phrase_time_limit=6):
        """Listen for speech input and return the recognized text."""
        with self.mic as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.WaitTimeoutError:
                print("No speech detected, continuing to listen...")
                return None
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return None
    
    def stop_speaking(self):
        """Stop current speech output."""
        self.engine.stop() 
