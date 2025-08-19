from flask import Flask, render_template, request
import cv2
import os
import tempfile
from safety_ai import get_safety_advice
from chat_ai import ask_gemini

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Extract key frames from video
def extract_frames(video_path, interval=60):
    frames = []
    cap = cv2.VideoCapture(video_path)
    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % interval == 0:
            frames.append(frame)
        count += 1
    cap.release()
    return frames[:7]

# Describe frame (basic crowd detection)
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def describe_frame(frame):
    boxes, _ = hog.detectMultiScale(frame, winStride=(8,8))
    people_count = len(boxes)
    description = f"Detected {people_count} people in this frame."
    if people_count > 50:
        description += " High crowd density, possible congestion."
    elif people_count > 20:
        description += " Moderate crowd density."
    else:
        description += " Low crowd density."
    return description

# Analyze video for initial safety advice
def analyze_video(video_path):
    frames = extract_frames(video_path)
    if not frames:
        return "No frames extracted from video."
    frame_descriptions = [f"Frame {i+1}: {describe_frame(frame)}" for i, frame in enumerate(frames)]
    scene_description = " ".join(frame_descriptions)
    advice = get_safety_advice(scene_description)
    global last_scene_description
    last_scene_description = scene_description
    return advice

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video = request.files.get("video")
        if video and video.filename != "":
            temp_video = os.path.join(tempfile.gettempdir(), video.filename)
            video.save(temp_video)
            result = analyze_video(temp_video)
            return render_template("result.html", result=result)
    return render_template("index.html")

# Chat route for user follow-up questions
@app.route("/chat", methods=["POST"])
def chat():
    question = request.form.get("question")
    if not question:
        return "No question provided."
    global last_scene_description
    answer = ask_gemini(last_scene_description, question)
    return render_template("result.html", result=answer)

if __name__ == "__main__":
    last_scene_description = ""
    app.run(debug=True)


