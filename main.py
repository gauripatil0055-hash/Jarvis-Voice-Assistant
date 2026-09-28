import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
from datetime import datetime
import sqlite3
from dotenv import load_dotenv

load_dotenv()
Gnewsapi = os.getenv("GNEWS_API_KEY")

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

# Database setup
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.db")
conn = sqlite3.connect(db_path,check_same_thread=False)
print("DATABASE PATH:", db_path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS command_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    command TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

# def processCommand(c)

def processCommand(c):
    print("COMMAND RECEIVED:", c)
    c = c.lower()

    cursor.execute(
        "INSERT INTO command_history (command) VALUES (?)",
        (c,)
    )
    conn.commit()

    if "open google" in c:
        webbrowser.open("https://google.com")

    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")

    elif c.startswith("play"):
        parts = c.split()

        if len(parts) > 1:
            song = parts[1]

            if song in musicLibrary.music:
                webbrowser.open(musicLibrary.music[song])
            else:
                speak("Sorry, song not found.")
        else:
            speak("Please tell me the song name.")

     # Gnewsapi

    elif "news" in c:
        url = "https://gnews.io/api/v4/top-headlines"

        params = {
            "category": "general",
            "lang": "en",
            "country": "in",
            "max": 5,
            "apikey": Gnewsapi
        }

        r = requests.get(url, params=params)

        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])

            for article in articles:
                speak(article["title"])

        else:
            speak("Sorry, I could not fetch the news.")

    #Weather

    elif "weather" in c:
        city = c.replace("weather", "").replace("in", "").strip()

        if not city:
          city = "Nashik"

        try:
          geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1}
          ).json()

          lat = geo["results"][0]["latitude"]
          lon = geo["results"][0]["longitude"]

          data = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m"
            }
           ).json()

          temp = data["current"]["temperature_2m"]
          speak(f"The temperature in {city} is {temp} degrees Celsius.")

        except:
          speak("Sorry, I could not fetch the weather.")        

    

     # Add task
    elif "add task" in c:
        task = c.replace("add task", "").strip()

        if task:
            cursor.execute(
                "INSERT INTO tasks (task) VALUES (?)",
                (task,)
            )
            conn.commit()
            speak("Task added successfully.")

        else:
            speak("Please tell me the task.")

     # Show task
    elif "show task" in c or "show tasks" in c:
        cursor.execute("SELECT task FROM tasks")

        tasks = cursor.fetchall()

        if tasks:
            speak("Your tasks are")

            for task in tasks:
                speak(task[0])

        else:
            speak("You have no tasks.")

    elif "delete task" in c:
        task = c.replace("delete task", "").strip()

        cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
        conn.commit()

        if cursor.rowcount > 0:
         speak("Task deleted successfully.")
        else:
         speak("Task not found.")        
       
     # Time and Date

    elif "time" in c:
        current_time = datetime.now().strftime("%I:%M %p")
        speak("The current time is " + current_time)

    elif "date" in c:
        current_date = datetime.now().strftime("%d %B %Y")
        speak("Today's date is " + current_date)

     # calculator   

    elif "calculate" in c:
     expression = c.replace("calculate", "").strip()

     try:
        result = eval(expression)
        speak("The answer is " + str(result))
     except:
          speak("Sorry, I could not calculate that.")  

     # Exit
      
    elif "exit" in c or "quit" in c or "stop" in c:
      speak("Goodbye! Have a nice day.")
      exit()       

    else:
      speak("Sorry, I don't understand that command.")



if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.4)
                audio = r.listen(source, timeout=4, phrase_time_limit=4)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))