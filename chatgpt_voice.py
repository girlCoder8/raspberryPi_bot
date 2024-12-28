import os
import openai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
import subprocess

yourtext = 'Welcome'
language = 'en'

openai.api_key = '<your_api_key>'
load_dotenv()
model = 'gpt-3.5-turbo'
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "<your_name_here>"
greetings = [f"how's it going {name}",
             "yes?",
             "Well, hello there, Queen of Coding - how's it going today?",
             f"Can you show me how you did that? {name}! Can you code in French?",
             f"Bonjour, Madame {name}! Comment ça va? I am speaking French?"]


# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for 'Hello there'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass


# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = openai.ChatCompletion.create(model="gpt-4.0",
                                                    messages=[{"role": "user", "content": f"{text}"}])
            response_text = response.choices[0].message.content
            print(response_text)

            # Speak the response
            print("speaking")
            os.system("espeak ' " + response_text + "'")
            engine.say(response_text)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break


# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
