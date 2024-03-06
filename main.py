import subprocess
import speech_recognition as sr
import numpy as np
import pygame
import webbrowser
from openai import OpenAI
import pywhatkit
import pygame

apikey = ''

def Speak(text, rate=150, volume=1.0, pause=15):
    voice = "en-us"
    subprocess.run(["espeak", "-v", voice, "-p", str(pause), text])

def play_beep_start():
    pygame.init()
    frequency = 600
    duration = 300
    
    # Parameters for the tone
    sample_rate = 44100
    num_samples = int(sample_rate * duration / 1000)
    buf = np.zeros((num_samples, 2), dtype=np.int16)
    max_val = np.iinfo(np.int16).max
    for i in range(num_samples):
        t = float(i) / sample_rate  # time in seconds
        buf[i][0] = int(max_val * np.sin(2 * np.pi * frequency * t))

    sound = pygame.sndarray.make_sound(buf)

    # Play the tone
    sound.play()
    pygame.time.wait(duration)
    pygame.quit()

def play_beep_listen():
    pygame.init()
    frequency = 400
    duration = 300
    
    # Parameters for the tone
    sample_rate = 44100
    num_samples = int(sample_rate * duration / 1000)
    buf = np.zeros((num_samples, 2), dtype=np.int16)
    max_val = np.iinfo(np.int16).max
    for i in range(num_samples):
        t = float(i) / sample_rate  # time in seconds
        buf[i][0] = int(max_val * np.sin(2 * np.pi * frequency * t))

    sound = pygame.sndarray.make_sound(buf)

    # Play the tone
    sound.play()
    pygame.time.wait(duration)
    pygame.quit()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        play_beep_start()
        print("My ears are all yours...")
        audio = r.listen(source)
    query = ''
    play_beep_listen()
    try:
        query = r.recognize_google(audio, language= 'en-US')
        print(f"Ravi said : {query}")
    except:
        print("Venom can't understand you!!")
        Speak("Sorry my lord, I couldn't understand you!")
    return query.lower()

def open_application(application):
    try:
        subprocess.Popen([application])
        print(f"Opened {application}")
    except FileNotFoundError:
        print(f"Error: {application} not found.")

def convo(query):
    global chatstr
    client = OpenAI(api_key=apikey)
    chatstr += f"Ravi : {query}\n Venom :"

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
        "role": "user",
        "content": chatstr
        },
    ],
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    try :
        Speak(response.choices[0].message.content)
        print(response.choices[0].message.content)
        chatstr += f"{response.choices[0].message.content}\n"
        
    except Exception as e:
        print(e)

def GoogleSearch(term):
    query = term.replace("venom", "")
    Query = str(query)
    pywhatkit.search(Query)
    Speak(f": Result of : {Query} is on this page...")

def Conversation():
    Speak("Greetings my lord")
    while True:
        userSaid = takeCommand()

        if "hello" in userSaid:
            Speak("hello")
        elif 'google search' in userSaid or 'search on google' in userSaid:
            userSaid = userSaid.replace("google search", "")
            userSaid = userSaid.replace("search on google", "")
            GoogleSearch(userSaid)
        elif "bye" in userSaid:
            Speak("goodbye")
        elif "how are you" in userSaid:
            Speak("doing well")
        elif "exit" in userSaid:
            Speak("ending program")
            Talk = False
        elif "open my email" in userSaid:
            Speak("This is where I would open your email.")
        elif ("open youtube" in userSaid or "open the youtube" in userSaid ):
            webbrowser.open("https://www.youtube.com")
            Speak("Opening Youtube...")
        elif ("open google" in userSaid or "open the google" in userSaid):
            webbrowser.open("https://www.google.com")
            Speak("Opening Google...")
        elif ("open notes" in userSaid or "open the notes" in userSaid or "open the note" in userSaid or "open note" in userSaid):
            webbrowser.open("https://keep.google.com/")
            Speak("Opening Google Notes...")  
        elif ("open satck overflow" in userSaid or "open the satck overflow" in userSaid):
            webbrowser.open("https://stackoverflow.com/")
            Speak("Opening stackoverflow...")
        elif "open calculator" in userSaid or "open calcu lator" in userSaid:
            open_application('gnome-calculator')
            Speak("Opening Calculator...")
        elif "open terminal" in userSaid:
            open_application('gnome-terminal')
            Speak("Opening Terminal...")
        elif "open file manager" in userSaid:
            open_application('nautilus')
            Speak("Opening File Manager...")
        elif "open text editor" in userSaid:
            open_application('gedit')
            Speak("Opening Text Editor...")
        elif "open web browser" in userSaid:
            open_application('firefox')
            Speak("Opening Fire Fox Web Browser...")
        elif ("open calculator" in userSaid or "open calcu lator" in userSaid):
            subprocess.Popen(['gnome-calculator'])
            Speak("Opening Chat GPT...")
        elif 'venom close' in userSaid or 'stop venom' in userSaid or 'venom stop' in userSaid:
            print("Are you sure? You want me to go?")
            Speak("Are you sure? You want me to go?")
            input = takeCommand()
            if "yes" in input or "go away" in input:
                print("I am going. Bye Bye!!")
                Speak("I am going. Byeee Byeee!")
                # break
                exit()
            elif "no" in input:
                print("Thank you, I am glad you choose to stay with me.")
                Speak("Thank you. I am glad you choose to stay with me...")
        else:
            convo(userSaid)

if __name__ == "__main__":
    Conversation()