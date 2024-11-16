# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import time
import os

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

todo_list = []

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""  # Initialize command
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print(f"Error: {e}")  # Optionally print the error for debugging
    return command


def get_weather(city):
    api_key = "3bb74be9c1350d35f0f360622810d3ad"
    # city = ["hyderabad","delhi", "Mumbai"]
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url).json()
    if response["cod"] != "404":
        weather = response["main"]
        temperature = weather["temp"] - 273.15  # Convert Kelvin to Celsius
        humidity = weather["humidity"]
        description = response["weather"][0]["description"]
        talk(f"The temperature in {city} is {temperature:.2f} degree Celsius, humidity is {humidity}%, and the weather is {description}.")
        print(weather)
    else:
        talk("City not found.")

def get_news():
    api_key = "349a2a75999b4f489a6f90fd22d7a711"
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url).json()
    if response["status"] == "ok":
        talk("Here are the top news headlines:")
        print(response)
        for article in response["articles"][:5]:  # Get top 5 news
            talk(article["title"])
    else:
        talk("I couldn't fetch the news at the moment.")

def set_reminder(task, delay):
    talk(f"Reminder set for {task}. I'll remind you in {delay} seconds.")
    time.sleep(delay)
    talk(f"Reminder: {task}")

def set_alarm(alarm_time):
    talk(f"Alarm set for {alarm_time}")
    while True:
        if datetime.datetime.now().strftime('%I:%M %p') == alarm_time:
            talk("It's time to wake up!")
            break

def add_todo(task):
    todo_list.append(task)
    talk(f"Added {task} to your to-do list.")

def show_todo():
    if todo_list:
        talk("Here's your to-do list:")
        for item in todo_list:
            talk(item)
    else:
        talk("Your to-do list is empty.")

def open_app(command):
    if 'notepad' in command:
        os.system('notepad')
    elif 'browser' in command:
        os.system('start chrome')
    elif 'spotify' in command:
        os.system('spotify')
        
    else:
        talk("I can't open that application.")

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time_now)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 5)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'I love you' in command:
        talk('I love you too')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        get_weather(city)
    elif 'news' in command:
        get_news()
    elif 'reminder' in command:
        task = command.replace('reminder', '').strip()
        set_reminder(task, 5)  # Example delay of 5 seconds; can modify
    elif 'alarm' in command:
        set_alarm("6:00 AM")  # Example alarm time; can modify
    elif 'add to-do' in command:
        task = command.replace('add to-do', '').strip()
        add_todo(task)
    elif 'show to-do' in command:
        show_todo()
    elif 'shutdown' in command:
        talk("Shutting down the system now.")
        os.system("shutdown /s /t 1")
    elif 'open' in command:
        open_app(command)
    else:
        talk('Please say the command again.')

while True:
    run_alexa()




