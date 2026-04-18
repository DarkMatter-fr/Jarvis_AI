import pyaudiowpatch as pyaudio
import sys
import pyttsx3
import speech_recognition as sr
import datetime
import time
import random  # Added for human-like delays
import undetected_chromedriver as uc  # The "Stealth" Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. THE MIC FIX
sys.modules['pyaudio'] = pyaudio

# 2. INITIALIZE THE MOUTH
def speak(audio):
    print(f"Jarvis: {audio}")
    engine = pyttsx3.init('sapi5')
    engine.say(audio)
    engine.runAndWait()
    engine.stop()

# 3. THE EARS
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

# 4. STEALTH SEARCH LOGIC
def search_google(query):
    speak(f"Searching for {query} on Google...")
    
    # Using undetected_chromedriver to hide from Google's bot detector
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    
    # Wait a random amount of time to look human
    time.sleep(random.uniform(1, 3))
    driver.get(f"https://www.google.com/search?q={query}")
    
    wait = WebDriverWait(driver, 15)
    try:
        # Looking for the main result container
        result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#search")))
        speak("Here is what I found, sir.")
        # Only reading the top snippet so it's not too long
        speak(result.text[:300]) 
    except:
        speak("I found the results, but they are protected by a security check. Please check the browser.")

def play_youtube(song):
    speak(f"Searching for {song} on YouTube")
    driver = uc.Chrome()
    driver.get(f"https://www.youtube.com/results?search_query={song}")
    
    wait = WebDriverWait(driver, 15)
    try:
        # Standard selector for the first video title
        video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-video-renderer a#video-title")))
        time.sleep(random.uniform(1, 2)) # Human-like pause before clicking
        video.click()
        speak("Video started, sir.")
    except:
        speak("I found the results, but I am unable to click the video.")

# --- MAIN EXECUTION LOOP ---
if __name__ == "__main__":
    speak("System initializing... All drivers online. I am ready, sir.")

    while True:
        query = takeCommand()

        if 'hello' in query:
            speak("Hello sir, how can I help you?")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {strTime}")

        elif 'play' in query:
            song = query.replace('play', '').strip()
            play_youtube(song)
          
        elif "search" in query:
            search_query = query.replace("search", "").strip()
            search_google(search_query)

        elif 'none' in query:
            # We skip this so he doesn't speak every time it's silent
            pass

        elif 'sleep' in query or 'exit' in query:
            speak("Goodbye sir. Have a productive day.")
            break

        