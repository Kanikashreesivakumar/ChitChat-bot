import speech_recognition as sr
from dotenv import load_dotenv
import os
import pyttsx3
import openai


load_dotenv() 
api_key=os.getenv("API_KEY")


openai.api_key = api_key
engine = pyttsx3.init()

def speak(text):
    
    engine.say(text)
    engine.runAndWait()

def listen():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
        except sr.RequestError:
            speak("There seems to be an issue with the speech recognition service.")
        except sr.WaitTimeoutError:
            speak("No input received. Please try again.")
    return None

def process_command(command):
    
    if command:
        try:
           
            response = openai.ChatCompletion.create(
                
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an intelligent voice assistant."},
                    {"role": "user", "content": command}
                ]
            )
            print(response.choices[0].message['content'])
            reply = response['choices'][0]['message']['content']
            speak(reply)
            print(f"Assistant: {reply}")
        except Exception as e:
            speak("I'm sorry, I encountered an issue.")
            print(f"Error: {e}")

if __name__ == "__main__":
    speak("Hello! I am your assistent friend... How can I help you today?")
    while True:
        user_command = listen()
        if user_command:
            print(f"You said: {user_command}")
            if "exit" in user_command.lower() or "stop" in user_command.lower():
                speak("Goodbye...have a nice day!")
                break
            process_command(user_command)