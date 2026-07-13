import os
import traceback
from google import genai

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))


def get_learning_recommendations(topic):
    prompt = f"""
    You are an AI tutor. The student wants to learn about: {topic}.
    Suggest a structured and adaptive learning path including key topics, order of learning, and resources (links, books, or videos).
    Include beginner, intermediate, and advanced levels if needed.
    """

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
        print("🧠 Gemini raw response:", response)

        if hasattr(response, "text"):
            return response.text
        else:
            return "❌ Could not extract content from Gemini response."
    except Exception as e:
        traceback.print_exc()  # ✅ This gives full error trace
        return f"❌ Error occurred: {str(e)}"