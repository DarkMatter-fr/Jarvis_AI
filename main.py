import eel
import threading
import datetime
import sys
import config
from modules import mouth, ears, brain, automation

# Initialize Eel
eel.init('.')

# Global lock to prevent multiple clicks from crashing the system
is_assistant_busy = False

def jarvis_greeting():
    """Performs the initial system check and greeting."""
    eel.sleep(1.0) # Wait for UI to stabilize
    if hasattr(eel, 'addMessage'):
        greeting = "All systems operational. I am standing by, sir."
        eel.addMessage('assistant', greeting)()
        mouth.speak(greeting)

@eel.expose
def process_voice_input():
    """Triggered by the UI Orb. Spawns the logic thread if not busy."""
    global is_assistant_busy
    if is_assistant_busy:
        print("System: Assistant is currently busy.")
        return
        
    is_assistant_busy = True
    threading.Thread(target=voice_logic_thread, daemon=True).start()

def voice_logic_thread():
    """The core execution loop."""
    global is_assistant_busy
    response = "I am not sure how to help with that, sir."
    
    try:
        # Step 1: Listening State
        eel.setAssistantState('listening')()
        eel.sleep(0.5) 
        
        query = ears.take_command()

        # Step 2: Validation
        if query == "none" or not query.strip():
            return # Skip to finally block

        eel.addMessage('user', query)()
        
        # Step 3: Thinking State
        eel.setAssistantState('thinking')()
        eel.sleep(0.5)

        # Step 4: Routing Logic
        question_words = ('who', 'what', 'where', 'when', 'why', 'how')

        if 'time' in query:
            response = f"Sir, the time is {datetime.datetime.now().strftime('%I:%M %p')}"
            
        elif 'play' in query:
            song = query.replace('play', '').replace('jarvis', '').strip()
            eel.addMessage('assistant', f"Opening YouTube for {song}...")()
            automation.play_youtube(song)
            response = f"Media feed for {song} is now active."

        elif 'search' in query or any(word in query for word in question_words):
            search_term = query.replace('search', '').replace('jarvis', '').strip()
            eel.addMessage('assistant', f"Searching archives for: {search_term}...")()
            
            # Selenium Retrieval
            raw_data = automation.search_google(search_term)
            # Gemini Summarization
            response = brain.summarize(raw_data, config.GEMINI_KEY)

        elif 'exit' in query or 'sleep' in query:
            mouth.speak("Shutting down, sir.")
            sys.exit()

        # Step 5: Output State
        eel.setAssistantState('speaking')()
        eel.addMessage('assistant', response)()
        mouth.speak(response)

    except Exception as e:
        print(f"Main Loop Error: {e}")
    finally:
        # Reset everything back to standby
        is_assistant_busy = False
        eel.setAssistantState('idle')()

if __name__ == "__main__":
    # block=False allows us to run Python logic after starting the UI
    eel.start('index.html', mode='chrome', size=(1000, 800), block=False)
    jarvis_greeting()
    
    while True:
        eel.sleep(1.0)