import google.generativeai as genai

API_KEY = "AIzaSyCLzJpyuH5iSb3g9HdFpVbQTntTXTzEbMc"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
  # Chat model

def ask_gemini(scene_description: str, user_message: str) -> str:
    prompt = f"Scene Description:\n{scene_description}\n\nQuestion: {user_message}"
    response = model.generate_content(prompt)
    return response.text
