import speech_recognition as sr

def take_command():
    """
    Captures audio input and converts it to text using Google Speech API.
    """
    r = sr.Recognizer()
    
    # Sensitivity Tuning
    r.dynamic_energy_threshold = True
    
    with sr.Microphone() as source:
        print("System: Calibrating noise...")
        # Adjusts to the room's background sound for 0.8 seconds
        r.adjust_for_ambient_noise(source, duration=0.8)
        
        print("Listening...")
        r.pause_threshold = 0.8 # Stop listening after 0.8s of silence
        
        try:
            # timeout: wait for speech to begin
            # phrase_time_limit: cut off long sentences
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
        except Exception:
            print("System: No speech detected.")
            return "none"

    try:
        print("Recognizing...")
        # language='en-in' for Indian accent; change to 'en-us' if preferred
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}")
        return query.lower()
    except Exception:
        print("System: Could not recognize speech.")
        return "none"