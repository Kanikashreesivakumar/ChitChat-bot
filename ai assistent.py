import speech_recognition as sr
from dotenv import load_dotenv
import os
import pyttsx3
from openai import OpenAI

# Loading api key from .env file
load_dotenv() 
api_key = os.getenv("API_KEY")

# initilizing api key
client = OpenAI(api_key=api_key)

# Initialzing text-speech model
engine = pyttsx3.init()

# Setting Voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to speak
def speak(text):  
    engine.say(text)
    engine.runAndWait()


def listen():
    
    # Creates intstance for speech recognition
    recognizer = sr.Recognizer()
    
    # Turning microphone on for listening
    with sr.Microphone() as source:
        print("Listening...")
        
        # Removing background noise
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")
            
            # Recongnise speech with gooogle's speech recognition API
            return recognizer.recognize_google(audio)
        
        # Unintelligble error
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
        # Netork issue error
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
        # Timeout error    
        except sr.WaitTimeoutError:
            speak("No input received. Please try again.")
    return None

def process_command(command):
    
    if command:
        try:
            
        # using openai API 
            response = client.chat.completions.create(
            messages=[
                {
                    "role": "assistant", "content": command,
                }
            ],
            model="gpt-4o-mini",
            )
            
            reply = response.choices[0].message.content
            print(f"Assistant: {reply}")
            speak(reply)
            
        except Exception as e:
            speak("I'm sorry, I encountered an issue.")
            print(f"Error: {e}")

if __name__ == "__main__":
    speak("Hello! I am your Lora... Your personal assistant...How can I help you today?")
    while True:
        user_command = listen()
        if user_command:
            print(f"You said: {user_command}")
            if any(keyword in user_command.lower() for keyword in ["exit", "stop", "quit"]):
                speak("Goodbye...have a nice day!")
                break

            process_command(user_command)
