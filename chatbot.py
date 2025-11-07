import pyttsx3
import speech_recognition as sr
import sounddevice as sd
import wavio
import numpy as np
import webbrowser
import pyjokes
import wikipedia
from datetime import datetime
import tempfile
import time
import winsound

# ---------------- TEXT-TO-SPEECH ----------------
def speak(text: str):
    """Print and speak the given text."""
    print(f"Jarvis: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 160)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"⚠️ Speech error: {e}")

# ---------------- VOICE INPUT ----------------
def listen(max_retries=3):
    """Listen to microphone; fallback to typing."""
    recognizer = sr.Recognizer()
    retries = 0

    while retries < max_retries:
        try:
            duration = 5  # seconds
            fs = 44100
            speak("Listening...")
            winsound.Beep(1000, 200)

            # record audio
            audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype=np.int16)
            sd.wait()

            # save temporary wav
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            wavio.write(temp_file.name, audio_data, fs, sampwidth=2)

            # recognize
            with sr.AudioFile(temp_file.name) as source:
                audio = recognizer.record(source)
            query = recognizer.recognize_google(audio, language="en-in")

            
            return query.lower()

        except sr.UnknownValueError:
            speak("Sorry, I didn’t catch that. Please type your command.")
            user_input = input("Type your command: ")
            return user_input.lower()

        except Exception as mic_error:
            retries += 1
            print(f"❌ Microphone error ({retries}/{max_retries}): {mic_error}")
            if retries < max_retries:
                speak("Trying again...")
                time.sleep(1.5)
            else:
                speak("Microphone not working. Please type your command.")
                user_input = input("Type your command: ")
                return user_input.lower()

def process_command(command):
    if "hello" in command or "hi" in command:
        speak("Hello! How can I assist you today?")

    elif "your name" in command:
        speak("I am Jarvis, your personal assistant.")

    elif "how are you" in command:
        speak("I’m doing great! How about you?")

    elif "joke" in command:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")

    elif "date" in command:
        today = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}.")

    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "open github" in command:
        speak("Opening GitHub.")
        webbrowser.open("https://github.com")

    elif "wikipedia" in command:
        try:
            topic = command.replace("wikipedia", "").strip()
            if not topic:
                speak("What should I search on Wikipedia?")
                topic = input("Enter topic: ")
                speak(f"Searching Wikipedia for {topic}.")
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except Exception:
            speak("Sorry, I couldn’t fetch that from Wikipedia.")

    elif any(x in command for x in ["stop", "bye", "exit", "quit"]):
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("Sorry, I’m still learning that command.")
    return True


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    time.sleep(0.8)
    active = True
    while active:
        command = listen()
        if command:
            active = process_command(command)
