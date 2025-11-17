import speech_recognition as sr
import pyttsx3
import pyaudio
import platform
from config import VOICE_SETTINGS, RECOGNITION_SETTINGS, LISTENING_SETTINGS

class SpeechHandler:
    def __init__(self, mic_device_index=None):
        """
        Initialize SpeechHandler with optional microphone device selection.
        
        Args:
            mic_device_index: Index of the microphone device to use. If None, uses default.
        """
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Initialize microphone with selected device or default
        if mic_device_index is not None:
            self.mic = sr.Microphone(device_index=mic_device_index)
            self.mic_device_index = mic_device_index
        else:
            self.mic = sr.Microphone()
            self.mic_device_index = None
        
        # Configure voice settings (platform-specific)
        self._configure_voice()
        self.engine.setProperty('rate', VOICE_SETTINGS['rate'])
        self.engine.setProperty('volume', VOICE_SETTINGS['volume'])
        
        # Configure recognition settings
        self.recognizer.energy_threshold = RECOGNITION_SETTINGS['energy_threshold']
        self.recognizer.dynamic_energy_threshold = RECOGNITION_SETTINGS['dynamic_energy_threshold']
        self.recognizer.pause_threshold = RECOGNITION_SETTINGS['pause_threshold']
        self.recognizer.operation_timeout = RECOGNITION_SETTINGS['operation_timeout']
    
    @staticmethod
    def list_audio_input_devices():
        """
        List all available audio input devices (microphones).
        
        Returns:
            list: List of dictionaries containing device info (index, name, channels)
        """
        devices = []
        try:
            p = pyaudio.PyAudio()
            device_count = p.get_device_count()
            
            for i in range(device_count):
                device_info = p.get_device_info_by_index(i)
                # Check if device has input channels (microphone)
                if device_info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxInputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate'])
                    })
            
            p.terminate()
        except Exception as e:
            print(f"Error listing audio devices: {e}")
        
        return devices
    
    @staticmethod
    def list_audio_output_devices():
        """
        List all available audio output devices (speakers).
        
        Returns:
            list: List of dictionaries containing device info (index, name, channels)
        """
        devices = []
        try:
            p = pyaudio.PyAudio()
            device_count = p.get_device_count()
            
            for i in range(device_count):
                device_info = p.get_device_info_by_index(i)
                # Check if device has output channels (speakers)
                if device_info['maxOutputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'channels': device_info['maxOutputChannels'],
                        'sample_rate': int(device_info['defaultSampleRate'])
                    })
            
            p.terminate()
        except Exception as e:
            print(f"Error listing audio devices: {e}")
        
        return devices
    
    @staticmethod
    def list_unique_audio_devices():
        """
        List all unique audio devices (input only, deduplicated by name).
        Returns devices that can be used as microphones.
        
        Returns:
            list: List of unique device dictionaries with the first occurrence of each device name
        """
        input_devices = SpeechHandler.list_audio_input_devices()
        
        if not input_devices:
            return []
        
        # Deduplicate by device name (normalized)
        seen_names = set()
        unique_devices = []
        
        for device in input_devices:
            # Normalize name for comparison (remove extra whitespace)
            normalized_name = ' '.join(device['name'].split())
            
            if normalized_name not in seen_names:
                seen_names.add(normalized_name)
                unique_devices.append(device)
        
        return unique_devices
    
    def _configure_voice(self):
        """Configure TTS voice based on platform."""
        system = platform.system()
        
        if system == "Windows":
            # Get available Windows voices
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer SAPI5 voices (Windows built-in)
                # Try to find a natural-sounding voice
                for voice in voices:
                    # Look for Microsoft voices (usually better quality)
                    if 'microsoft' in voice.name.lower() or 'zira' in voice.name.lower() or 'david' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        print(f"Using voice: {voice.name}")
                        return
                # Fallback to first available voice
                if voices:
                    self.engine.setProperty('voice', voices[0].id)
                    print(f"Using voice: {voices[0].name}")
        elif system == "Darwin":  # macOS
            # Use configured macOS voice
            self.engine.setProperty('voice', VOICE_SETTINGS['voice'])
        else:  # Linux
            # Use default Linux voice
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[0].id)
    
    @staticmethod
    def print_audio_devices():
        """
        Print all available unique audio devices (microphones) in a simplified format.
        """
        devices = SpeechHandler.list_unique_audio_devices()
        
        print("\n" + "="*60)
        print("AVAILABLE AUDIO DEVICES (Microphones):")
        print("="*60)
        
        if not devices:
            print("No devices found.")
        else:
            for device in devices:
                print(f"  [{device['index']}] {device['name']}")
        
        print("="*60 + "\n")
    
    def calibrate_microphone(self, duration=0.5):
        """Calibrate microphone for ambient noise."""
        print("Calibrating microphone for ambient noise...")
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=duration)
        print("Calibration complete. Jarvis is ready!")
    
    def listen_for_speech(self, timeout=None, phrase_time_limit=None):
        """Listen for speech input and return the recognized text."""
        # Use configured defaults if not specified
        if timeout is None:
            timeout = LISTENING_SETTINGS['timeout']
        if phrase_time_limit is None:
            phrase_time_limit = LISTENING_SETTINGS['phrase_time_limit']
            
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
    
    def speak(self, text):
        """Convert text to speech and wait for it to complete."""
        if not text or not text.strip():
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            # Add a small delay after TTS completes to ensure audio finishes
            import time
            time.sleep(0.3)  # Small buffer to ensure audio playback completes
        except Exception as e:
            print(f"Error in TTS: {e}")
            # Fallback to print if TTS fails
            print(f"Jarvis (TTS failed): {text}")
    
    def list_available_voices(self):
        """List all available TTS voices."""
        try:
            voices = self.engine.getProperty('voices')
            voice_list = []
            for i, voice in enumerate(voices):
                voice_list.append({
                    'index': i,
                    'id': voice.id,
                    'name': voice.name,
                    'languages': getattr(voice, 'languages', [])
                })
            return voice_list
        except Exception as e:
            print(f"Error listing voices: {e}")
            return []
    
    def set_voice(self, voice_index=None, voice_id=None):
        """
        Set the TTS voice by index or ID.
        
        Args:
            voice_index: Index of the voice in the voices list
            voice_id: ID of the voice to use
        """
        try:
            voices = self.engine.getProperty('voices')
            if not voices:
                return False, "No voices available"
            
            if voice_id:
                # Find voice by ID
                for voice in voices:
                    if voice.id == voice_id:
                        self.engine.setProperty('voice', voice.id)
                        return True, f"Changed voice to {voice.name}"
                return False, f"Voice ID not found: {voice_id}"
            
            elif voice_index is not None:
                # Use voice by index
                if 0 <= voice_index < len(voices):
                    voice = voices[voice_index]
                    self.engine.setProperty('voice', voice.id)
                    return True, f"Changed voice to {voice.name}"
                else:
                    return False, f"Invalid voice index. Available: 0-{len(voices)-1}"
            
            return False, "Please provide either voice_index or voice_id"
        except Exception as e:
            return False, f"Error changing voice: {str(e)}"
    
    def stop_speaking(self):
        """Stop current speech output."""
        self.engine.stop() 