import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
_model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")


def explain_topic(topic: str) -> str:
    try:
        prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
        response = _model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠ Error in Explanation: {e}"
