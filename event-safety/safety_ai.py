import google.generativeai as genai

# ✅ Direct API key (replace "YOUR_API_KEY" with your key)
API_KEY = "AIzaSyCLzJpyuH5iSb3g9HdFpVbQTntTXTzEbMc"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_safety_advice(scene_description: str) -> str:
    response = model.generate_content(
        scene_description
    )
    return response.text

























