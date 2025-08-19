import streamlit as st
import cv2
import os
import tempfile
from safety_ai import get_safety_advice
from chat_ai import ask_gemini  # Your chat Gemini module

st.set_page_config(page_title="Event Safety AI", page_icon="⚠️", layout="centered")
st.title("Event Safety Video Analyzer 🚨")

# Upload video
video_file = st.file_uploader("Upload Event Video (any format)", type=["mp4","avi","mov","mkv"])

# Store last scene description globally
if 'last_scene_description' not in st.session_state:
    st.session_state.last_scene_description = ""

if video_file:
    st.video(video_file)

    # Save temporarily
    temp_video_path = os.path.join(tempfile.gettempdir(), video_file.name)
    with open(temp_video_path, "wb") as f:
        f.write(video_file.getbuffer())

    st.info("Analyzing video, please wait... ⏳")

    # Extract key frames
    cap = cv2.VideoCapture(temp_video_path)
    frame_count = 0
    key_frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 60 == 0:
            key_frames.append(frame_count)
        frame_count += 1
    cap.release()

    scene_description = f"Video has {len(key_frames)} key frames for crowd analysis."
    st.session_state.last_scene_description = scene_description  # Save for chat

    # Call Gemini AI for initial safety advice
    advice = get_safety_advice(scene_description)

    st.success("Analysis Complete ✅")
    st.subheader("Safety Advice / Warnings")
    st.write(advice)

    st.info("Frames analyzed (indexes): " + ", ".join(map(str, key_frames)))

    # --- Chat interface ---
    st.subheader("Ask AI about this scene")
    user_question = st.text_input("Your Question:")
    if st.button("Send Question"):
        if user_question.strip() != "":
            # Use last scene description + user question
            response = ask_gemini(st.session_state.last_scene_description, user_question)
            st.markdown(f"**AI Answer:** {response}")

