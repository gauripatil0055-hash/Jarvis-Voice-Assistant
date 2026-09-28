# JARVIS – Voice-Based Personal Assistant

## Project Overview

JARVIS is a Python-based voice assistant that accepts voice commands, processes them, and performs different tasks such as opening websites, playing music, fetching live news, checking weather, managing tasks, performing calculations, and providing time and date information.

## Features

- Voice command recognition
- Text-to-speech response
- Open Google, YouTube, Facebook and LinkedIn
- Music playback
- Live news using GNews API
- Weather information using Open-Meteo API
- Add, show and delete tasks
- SQLite database for task storage
- Command history
- Calculator
- Current time and date
- Error handling
- Secure API key management using `.env`

## Technologies Used

- Python
- SpeechRecognition
- pyttsx3
- gTTS
- pygame
- Requests
- REST APIs
- SQLite
- Open-Meteo API
- GNews API

## Project Architecture

Voice Input  
↓  
Speech Recognition  
↓  
Command Processing  
↓  
Action / API / Database  
↓  
Voice Response

## Database

SQLite is used to store:

- Tasks
- Command history

## API Integration

### GNews API
Used to retrieve live news.

### Open-Meteo API
Used to retrieve weather information without requiring an API key.

## Security

The GNews API key is stored in a `.env` file instead of directly inside the Python source code.

The `.env` file is excluded using `.gitignore`.

## How to Run

1. Clone or download the project.
2. Create a Python virtual environment.
3. Install required packages:

```bash
pip install -r requirements.txt


4. Create a .env file and add:
    
    GNEWS_API_KEY=YOUR_API_KEY

5. Run:

    python main.py

6. Say "Jarvis" and give a command.

Example Commands

- "Jarvis, open Google"
- "Jarvis, play[song name]"
- "Jarvis, show news"
- "Jarvis, weather in Nashik"
- "Jarvis, add task complete project"
- "Jarvis, show tasks"
- "Jarvis, delete task complete project"
- "Jarvis, what is the time?"
- "Jarvis, what is today's date?"
- "Jarvis, calculate 25 + 10"


# Future Scope

- Reminders and notifications
- More system automation
- Natural Language Processing
- Additional APIs and services

Author

 Gauri Patil (MSc (CS)Student)

 