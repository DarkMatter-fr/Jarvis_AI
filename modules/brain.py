# modules/brain.py
from google import genai




def summarize(messy_text, api_key):
    client = genai.Client(api_key=api_key)
    try:
        # gemini-3-flash-preview is the recommended 2026 free model
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"Jarvis, summarize this search data into 3 conversational sentences: {messy_text}"
        )
        return response.text
    except Exception as e:
        return f"Sir, I couldn't process the summary. Error: {e}"