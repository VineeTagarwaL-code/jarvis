# Jarvis - AI Voice Assistant

A modular, intelligent voice assistant inspired by Iron Man's AI, built with Python. Jarvis can perform various tasks through voice commands, including web searches, calculations, time queries, and more.

## 🏗️ Project Structure

The project has been refactored into a modular architecture for better maintainability and extensibility:

```
jarvis/
├── main.py              # Main entry point
├── jarvis.py            # Core Jarvis class
├── config.py            # Configuration and settings
├── speech_handler.py    # Speech recognition and TTS
├── ai_handler.py        # OpenAI API and function calling
├── tools.py             # Available functions/tools
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .env                # Environment variables (create this)
```

## 🚀 Features

- **Voice Recognition**: Real-time speech-to-text using Google Speech Recognition
- **Text-to-Speech**: Natural voice output using edge-tts
- **AI Processing**: OpenAI GPT-4 integration with function calling
- **Web Search**: Real-time information using Perplexity API
- **Modular Design**: Clean separation of concerns for easy maintenance
- **Extensible**: Easy to add new tools and capabilities

## 🛠️ Available Tools

1. **Time**: Get current system time
2. **Calculator**: Perform mathematical calculations
3. **Web Search**: Search for real-time information
4. **URL Opener**: Open websites in browser

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd jarvis
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PERPLEXITY_API_KEY=your_perplexity_api_key_here
   ```

## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### Programmatic Usage
```python
from jarvis import Jarvis

# Create Jarvis instance
jarvis = Jarvis()

# Start listening for voice commands
jarvis.start()

# Or process text commands
response = jarvis.process_text_command("jarvis what time is it")
```

## 🗣️ Voice Commands

- **"Jarvis, what time is it?"** - Get current time
- **"Jarvis, calculate 15 plus 27"** - Perform calculations
- **"Jarvis, what's the weather in New York?"** - Web search
- **"Jarvis, open google.com"** - Open websites
- **"stop"** - Exit Jarvis

## 🔧 Configuration

All settings are centralized in `config.py`:

- **Voice Settings**: Voice type, rate, volume
- **Recognition Settings**: Energy threshold, pause threshold
- **API Settings**: Model selection, token limits, temperature
- **System Prompt**: AI personality and behavior

## 🏗️ Architecture

### Core Components

1. **Jarvis Class** (`jarvis.py`): Main orchestrator
2. **SpeechHandler** (`speech_handler.py`): Speech I/O management
3. **AIHandler** (`ai_handler.py`): OpenAI integration and function calling
4. **Tools** (`tools.py`): Available functions and their definitions

### Adding New Tools

1. **Add function to `tools.py`**:
   ```python
   def my_new_function(param):
       # Your function logic
       return "Result"
   ```

2. **Add to FUNCTIONS list**:
   ```python
   {
       "name": "my_new_function",
       "description": "Description of what it does",
       "parameters": {
           "type": "object",
           "properties": {
               "param": {"type": "string"}
           },
           "required": ["param"]
       }
   }
   ```

3. **Add to FUNCTION_MAP**:
   ```python
   FUNCTION_MAP = {
       # ... existing functions
       "my_new_function": my_new_function
   }
   ```

## 🔍 Troubleshooting

### Common Issues

1. **Microphone not working**: Check system permissions and microphone settings
2. **API errors**: Verify API keys in `.env` file
3. **Speech recognition issues**: Adjust energy threshold in `config.py`

### Debug Mode

Enable debug output by modifying the speech handler settings in `config.py`.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Perplexity for web search capabilities
- Google Speech Recognition API
- pyttsx3 for text-to-speech 
