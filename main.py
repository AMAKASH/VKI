# Necessary Imports

from person import Person
from threading import Thread
import pickle
import sys
import time
import speech_recognition as sr
#import cv2
#import face_recognition
import pyttsx3
import os
import webbrowser as wb

# Global Variables for usage of all threads
global_shutdown = False
known_persons = []
audios = []
processing_texts = []
responses = []
web_site_list = {}


# Worker functions

def listener():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Listening.......")
            audio = r.listen(source, phrase_time_limit=5)
            audios.append(audio)


def voice_processor():
    r = sr.Recognizer()
    while True:
        processing_text = ""
        if len(audios) != 0:
            audio = audios.pop(0)
            try:
                print("Processing audio.......")
                processing_text = r.recognize_google(audio, language="en")
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            if processing_text != "":
                processing_text = processing_text.lower()
                processing_texts.append(processing_text)


def command_text_processor():
    while True:
        if len(processing_texts) != 0:
            text = processing_texts.pop(0)
            print(text)
            arr = text.split()
            if "terminate" in arr:
                global global_shutdown
                global_shutdown = True
                responses.append("Terminating Program.")
            elif "launch" in arr:
                index = arr.index("launch")
                arr = arr[index + 1:]
                run(arr)
            elif "open" in arr:
                index = arr.index("open")
                arr = arr[index + 1:]
                open_web(arr)
            elif "search" in arr:
                index = arr.index("search")
                arr = arr[index + 1:]
                if "for" in arr:
                    arr.remove("for")
                search(arr)


def speaker():
    engine = pyttsx3.init()
    engine.setProperty('rate', 185)
    while True:
        if len(responses) != 0:
            response = responses.pop(0)
            engine.say(response)
            engine.runAndWait()


# Supporting functions

def run(arr):
    # print(arr)
    arg = "Database/Other/Program Shortcuts/"
    response = "Launching "
    for s in arr:
        arg += s + " "
        response += s + " "
    arg = arg[:-1]
    arg += ".lnk"
    path = os.path.abspath(arg)
    try:
        os.startfile(path)
    except FileNotFoundError:
        print("File not Found")
        response = "File not Found"
    response += "."
    responses.append(response)


def open_web(arr):
    key = arr.pop(0)
    val = web_site_list.get(key)
    if val is None:
        print("Not in dictionary")
        response = "Can not find website in dictionary."
    else:
        wb.open_new(val)
        response = f"Opening {key} now."
    responses.append(response)


def search(arr):
    if len(arr) != 0:
        response = "Searching for "
        phrase = ""
        while len(arr) != 1:
            s = arr.pop(0)
            phrase += s + "+"
            response += s + " "
        s = arr.pop(0)
        phrase += s
        response += s
        wb.open_new("https://www.google.com/search?q=" + phrase)
        # print(phrase)
        responses.append(response)


def file_reader(location):
    try:
        with open(location, "rb") as f:
            file = pickle.load(f)
            return file
    except FileNotFoundError:
        print("File not found")
        return None


# working threads

listener_thread = Thread(target=listener)
listener_thread.setDaemon(True)

voice_processor_thread = Thread(target=voice_processor)
voice_processor_thread.setDaemon(True)

command_text_processor_thread = Thread(target=command_text_processor)
command_text_processor_thread.setDaemon(True)

speaker_thread = Thread(target=speaker)
speaker_thread.setDaemon(True)

# testing codes
web_site_list.update(file_reader("./Database/Other/webList.p"))
listener_thread.start()
voice_processor_thread.start()
command_text_processor_thread.start()
speaker_thread.start()
count = 1
while count < 60:
    if global_shutdown:
        time.sleep(2)
        quit()
    print(".")
    time.sleep(1)
    count = count + 1
