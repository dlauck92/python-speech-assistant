import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from time import ctime
from multiprocessing import Process

r = sr.Recognizer()

def play_sound(file):
    playsound.playsound(file)

def vito_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    audio_file = f'audio-{random.randint(1, 1000000)}.mp3'
    tts.save(audio_file)

    # Play sound in a separate process
    p = Process(target=play_sound, args=(audio_file,))
    p.start()
    p.join()  # Wait for the sound to finish playing

    # Now remove the file safely
    os.remove(audio_file)

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            vito_speak(ask)
        audio = r.listen(source)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            vito_speak("Sorry, I don't understand what you said")
        except sr.RequestError:
            vito_speak("Sorry, my speech service is down.")
        return voice_data

def respond(voice_data):
    if 'what is your name' in voice_data:
        vito_speak("My name is Vito")
    if 'what time is it' in voice_data:
        vito_speak(f'The current time is {ctime()}')
    if 'search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.open(url)
        vito_speak(f"Here's what I found for {search}")
    if 'find location' in voice_data:
        location = record_audio('What do you want to know the location of?')
        url = 'https://google.nl/maps/place/' + location
        webbrowser.open(url)
        vito_speak(f"Here's the location of {location}")
    if 'exit' in voice_data:
        vito_speak("Goodbye!")
        exit()

# Windows multiprocessing fix
if __name__ == "__main__":
    time.sleep(1)
    vito_speak("How can I help you?")
    while True:
        voice_data = record_audio()
        respond(voice_data)
