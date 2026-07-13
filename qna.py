import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def answer_question_with_gemini(question: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-3.5-flash")
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"⚠ Error in QnA: {e}"
