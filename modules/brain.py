# modules/brain.py
from google import genai

def summarize(raw_data, api_key):
    # If this fails, the key wasn't passed from main.py
    if not api_key or api_key == "":
        return "Sir, the Gemini API key is missing from my configuration."

    client = genai.Client(api_key=api_key)
    
    # Rest of your generation logic...
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Summarize this for a voice assistant: {raw_data}"
    )
    return response.text