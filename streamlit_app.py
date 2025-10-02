import streamlit as st
from youtube_to_amv import download_and_convert

# Page setup
st.set_page_config(page_title="🎬 YouTube → AMV Converter", page_icon="🎵", layout="wide")

# Custom CSS for background + styling
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #ff758c, #ff7eb3);
        color: white;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .stButton>button {
        background-color: #ff4b5c;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 10px;
        border: none;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """
    , unsafe_allow_html=True
)

# Title
st.title("🎶 YouTube → AMV Converter 🎥✨")

# Input URL
url = st.text_input("🔗 Enter YouTube URL:")

# File format options
format_choice = st.selectbox("🎞 Choose output format:", ["mp4", "avi", "mov", "mkv", "webm", "flv", "wmv", "gif"])

# Convert button
if st.button("🚀 Convert Now!"):
    if url:
        with st.spinner("Downloading & converting... 🎬"):
            output_file = download_and_convert(url, format_choice)
            if output_file:
                st.success("✅ Conversion complete!")
                st.download_button("📥 Download AMV", open(output_file, "rb"), file_name=output_file)
            else:
                st.error("⚠️ Conversion failed. Try another link.")
    else:
        st.warning("Please enter a YouTube link first.")
