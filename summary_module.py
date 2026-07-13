from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_text(text):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"Summarize the following paragraph in a few concise sentences:\n\n{text}"
    )
    return response.text