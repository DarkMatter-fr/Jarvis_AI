import pyaudiowpatch as pyaudio
import sys
import pyttsx3
import speech_recognition as sr
import datetime
import time
import random  # Added for human-like delays
from google import genai as client
import os
import warnings
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

from google import genai

# 1. Use the standard client initialization
MODEL_NAME = "gemini-3-flash-preview"
client = genai.Client(api_key="AIzaSyCvt7KYnPKJSgB-PjH16uCqAeRrsxWFv3A")

def summarize_with_gemini(messy_text):
    # Cleaning the text helps prevent "Token Vomit" errors
    clean_text = " ".join(messy_text[:3000].split())
    
    # Try the request with a simple retry loop for 2026 stability
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=f"Jarvis, summarize this into 3 professional sentences for your master: {clean_text}"
            )
            return response.text
        except Exception as e:
            if "429" in str(e):
                print("Rate limit hit, retrying in 2 seconds...")
                time.sleep(2)
            elif "503" in str(e) or "500" in str(e):
                print("Google server issue, retrying...")
                time.sleep(1)
            else:
                print(f"Gemini error: {e}")
                break
                
    return "Sir, my neural link is experiencing high latency. I suggest reading the screen for now."
# 4. STEALTH SEARCH LOGIC


def search_google(query):
    # This silences the annoying 'ResourceWarning' from the console
    warnings.filterwarnings("ignore", category=ResourceWarning)
    
    speak(f"Searching for {query} on Google...")
    
    options = uc.ChromeOptions()
    # We use a persistent profile to look more 'human' to Google
    driver = uc.Chrome(options=options, use_subprocess=False) 
    
    try:
        driver.get(f"https://www.google.com/search?q={query}")
        wait = WebDriverWait(driver, 15)
        
        # 2026-safe selector: Looking for the main result text
        result_element = wait.until(EC.presence_of_element_located((By.ID, "search")))
        raw_text = result_element.text[:2500]
        
        speak("I have the results, sir. Sending to Gemini for analysis.")
        
        # Now pass it to your Gemini function
        summary = summarize_with_gemini(raw_text)
        speak(summary)
        
    except Exception as e:
        print(f"Operational Error: {e}")
        speak("Sir, I found the data, but my connection to the browser was interrupted.")
        
    finally:
        # The 'WinError 6' fix: We force a close and catch the error if it fails
        try:
            driver.close()
            time.sleep(0.5)
            driver.quit()
        except OSError:
            # This 'eats' the WinError 6 so it doesn't crash your main Jarvis loop
            pass

def play_youtube(video_query):
    speak(f"Playing {video_query} on YouTube...")
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options, use_subprocess=False)
    
    try:
        driver.get(f"https://www.youtube.com/results?search_query={video_query}")
        wait = WebDriverWait(driver, 15)
        
        # Click the first video result
        video = wait.until(EC.element_to_be_clickable((By.ID, "video-title")))
        video.click()
        
    except Exception as e:
        print(f"Error playing YouTube: {e}")
        speak("Sir, I encountered an issue while trying to play the song.")
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
            video_query = query.replace('play', '').strip()
            play_youtube(video_query)
          
        elif "search" in query or "what" in query or "who" in query or "how" in query or "why" in query or "when" in query:
            search_query = query.replace("search", "").strip()
            search_google(search_query)

        elif 'none' in query:
            # We skip this so he doesn't speak every time it's silent
            pass

        elif 'sleep' in query or 'exit' in query:
            speak("Goodbye sir. Have a productive day.")
            break

        