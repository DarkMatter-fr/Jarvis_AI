import pyaudiowpatch as pyaudio
import sys
import pyttsx3
import speech_recognition as sr
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. THE MIC FIX (Crucial for Python 3.14/3.12 compatibility)
sys.modules['pyaudio'] = pyaudio

# 2. INITIALIZE THE MOUTH (Fresh engine to prevent audio driver hanging)
def speak(audio):
    print(f"Jarvis: {audio}")
    engine = pyttsx3.init('sapi5')
    engine.say(audio)
    engine.runAndWait()
    engine.stop()

# 3. THE EARS (Voice Recognition)
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        return "none"
    return query.lower()

# 4. YOUTUBE AUTOMATION LOGIC
def play_youtube(song):
    speak(f"Searching for {song} on YouTube")
    driver = webdriver.Chrome()
    driver.get(f"https://www.youtube.com/results?search_query={song}")
    
    wait = WebDriverWait(driver, 10)
    try:
        # Tries to find the first clickable video title
        video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-video-renderer a#video-title")))
        video.click()
        speak("Video started, sir.")
        # Keeps browser open; if you want it to close automatically, uncomment the line below
        # time.sleep(30); driver.quit()
    except:
        speak("I found the results, but I am unable to click the video.")

# --- MAIN EXECUTION LOOP ---
if __name__ == "__main__":
    speak("System initializing... All drivers online. I am ready, sir.")

    while True:
        query = takeCommand()

        # Command: Greetings
        if 'hello' in query:
            speak("Hello sir, how can I help you?")

        # Command: Time
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {strTime}")

        # Command: YouTube
        elif 'play' in query:
            song = query.replace('play', '').strip()
            play_youtube(song)

        # Command: Shutdown Jarvis
        elif 'sleep' in query or 'exit' in query:
            speak("Goodbye sir. Have a productive day.")
            break