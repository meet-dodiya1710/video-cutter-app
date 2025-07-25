# subclipped.py
import streamlit as st
from moviepy import VideoFileClip
from datetime import datetime
import os

# ---------- Page Config ----------
st.set_page_config(page_title="Smart Video Cutter", page_icon="✂️", layout="centered")

# ---------- Styling ----------
st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .stButton>button {
        background-color: #f0f0f0;
        color: #000;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px;
        border: 1px solid #ccc;
    }
    .stDownloadButton>button {
        background-color: #f0f0f0 !important;
        color: #000 !important;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 6px;
        border: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Helper Functions ----------
def time_to_seconds(time_str):
    try:
        time_obj = datetime.strptime(time_str.strip(), "%H:%M:%S.%f")
    except ValueError:
        try:
            time_obj = datetime.strptime(time_str.strip(), "%H:%M:%S")
        except ValueError:
            raise ValueError("Time must be in HH:MM:SS or HH:MM:SS.mmm format.")
    return (
        time_obj.hour * 3600
        + time_obj.minute * 60
        + time_obj.second
        + time_obj.microsecond / 1e6
    )

def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

def cut_video(video_path, start_time, end_time, output_filename="cut_output.mp4"):
    video = VideoFileClip(video_path)
    cut_video = video.subclipped(start_time, end_time)
    cut_video.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    return output_filename

# ---------- Main App ----------
def main():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2921/2921222.png", width=80)
        st.title("🎥 Smart Video Cutter")
        st.markdown(
            """
            Trim your video with just a few clicks!  
            ✅ Upload a video (mp4, mov, avi, mkv, webm)  
            ✅ Enter start and end time  
            ✅ Get your trimmed video 🎉
            """
        )
        st.markdown("---")
        st.info("Made with ❤️ using Streamlit + MoviePy")

    st.title("✂️ Video Trimmer Tool")

    uploaded_file = st.file_uploader(
        "📤 Upload Video File", 
        type=["mp4", "mov", "avi", "mkv", "webm"]
    )

    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)
        st.success("✅ Video uploaded successfully!")

        col1, col2 = st.columns(2)
        with col1:
            start_time_str = st.text_input("🕐 Start Time", placeholder="Enter start time (e.g. HH:MM:SS.mmm)")

        with col2:
            end_time_str = st.text_input("🕙 End Time",  placeholder="Enter end time (e.g. HH:MM:SS.mmm)")

        if st.button("Trim Video"):
            try:
                start_sec = time_to_seconds(start_time_str)
                end_sec = time_to_seconds(end_time_str)

                if start_sec >= end_sec:
                    st.error("❌ Start time must be less than end time.")
                else:
                    with st.spinner("🔄 Trimming video..."):
                        output_path = "cut_output.mp4"
                        cut_video(file_path, start_sec, end_sec, output_path)

                    st.success("✅ Video trimmed successfully!")
                    with open(output_path, "rb") as f:
                        st.download_button(
                            "📥 Download Trimmed Video",
                            f,
                            file_name="cut_output.mp4"
                        )

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")

if __name__ == "__main__":
    main()
