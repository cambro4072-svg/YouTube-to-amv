import streamlit as st
import os
import subprocess
import tempfile
from youtube_to_amv import download_youtube, convert_to_amv

st.set_page_config(
    page_title="Video Converter Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    div[data-testid="stMarkdownContainer"] h1 {
        color: white;
        text-align: center;
        font-size: 3.5em;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5em;
    }
    div[data-testid="stMarkdownContainer"] h2 {
        color: white;
        text-align: center;
        font-weight: 400;
        margin-bottom: 2em;
    }
    .stRadio > div {
        background: rgba(255,255,255,0.1);
        padding: 1em;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    .stRadio label {
        color: white !important;
    }
    .stSelectbox label {
        color: white !important;
        font-weight: 600;
    }
    .stTextInput label {
        color: white !important;
        font-weight: 600;
    }
    .stFileUploader label {
        color: white !important;
        font-weight: 600;
    }
    .stNumberInput label {
        color: white !important;
        font-weight: 600;
    }
    .stCheckbox label {
        color: white !important;
    }
    .stFileUploader > div {
        background: rgba(255,255,255,0.1);
        padding: 2em;
        border-radius: 10px;
        border: 2px dashed rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a6f 100%);
        color: white;
        font-size: 1.2em;
        font-weight: 600;
        padding: 0.8em 2em;
        border: none;
        border-radius: 50px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    .info-card {
        background: rgba(255,255,255,0.1);
        padding: 1.5em;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        color: white;
        margin-top: 2em;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🎬 Video Converter Pro</h1>", unsafe_allow_html=True)
st.markdown("<h2>Transform your videos with ease - Download from YouTube or upload your own files</h2>", unsafe_allow_html=True)

col_left, col_center, col_right = st.columns([1, 3, 1])

with col_center:
    conversion_mode = st.radio(
        "Choose conversion mode:",
        ["📥 YouTube Download", "📁 File Upload"],
        horizontal=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if conversion_mode == "📥 YouTube Download":
        youtube_url = st.text_input("🔗 Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
        uploaded_file = None
    else:
        youtube_url = None
        uploaded_file = st.file_uploader(
            "📤 Upload video file",
            type=["mp4", "avi", "mkv", "mov", "webm", "flv", "wmv", "mpg", "mpeg", "3gp", "m4v", 
                  "ogv", "asf", "rm", "rmvb", "vob", "mts", "m2ts", "divx", "xvid", "f4v", 
                  "amv", "swf", "mpv", "qt"],
            help="Upload any video file to convert to your desired format"
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    format_option = st.selectbox(
        "🎯 Output Format:",
        ["AMV (160x120, 12fps)", "MP4", "AVI", "MKV", "WEBM", "MOV", "FLV", "Custom Settings"],
        help="Choose a preset format or custom settings"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if format_option == "Custom Settings" or format_option.startswith("AMV"):
        col1, col2 = st.columns(2)
        with col1:
            width = st.number_input("📏 Width", value=160 if "AMV" in format_option else 1280, min_value=80, max_value=3840)
            fps = st.number_input("🎞️ FPS", value=12 if "AMV" in format_option else 30, min_value=1, max_value=60)
        with col2:
            height = st.number_input("📐 Height", value=120 if "AMV" in format_option else 720, min_value=60, max_value=2160)
            include_audio = st.checkbox("🔊 Include Audio", value=True)
        
        if format_option.startswith("AMV"):
            file_ext = "amv"
            output_filename = st.text_input("💾 Output filename:", value="output.amv")
        else:
            file_ext = st.text_input("📝 File extension:", value="mp4").lower()
            output_filename = st.text_input("💾 Output filename:", value=f"output.{file_ext}")
    else:
        file_ext = format_option.lower()
        output_filename = st.text_input("💾 Output filename:", value=f"output.{file_ext}")
        include_audio = st.checkbox("🔊 Include Audio", value=True)
        width = None
        height = None
        fps = None
    
    if not output_filename.endswith(f".{file_ext}"):
        output_filename = f"{output_filename}.{file_ext}"
    
    st.markdown("<br>", unsafe_allow_html=True)

def convert_video(input_path, output_path, format_ext, width=None, height=None, fps=None, include_audio=True):
    cmd = ["ffmpeg", "-y", "-i", input_path]
    
    if width and height:
        cmd.extend(["-vf", f"scale={width}:{height}"])
    
    if fps:
        cmd.extend(["-r", str(fps)])
    
    if format_ext == "amv":
        cmd.extend(["-c:v", "mpeg4", "-b:v", "256k"])
        if include_audio:
            cmd.extend(["-c:a", "mp2", "-ar", "22050"])
        else:
            cmd.append("-an")
    elif format_ext == "mp4":
        cmd.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "23"])
        if include_audio:
            cmd.extend(["-c:a", "aac", "-b:a", "128k"])
        else:
            cmd.append("-an")
    elif format_ext == "avi":
        cmd.extend(["-c:v", "mpeg4"])
        if include_audio:
            cmd.extend(["-c:a", "mp3", "-b:a", "128k"])
        else:
            cmd.append("-an")
    elif format_ext == "webm":
        cmd.extend(["-c:v", "libvpx-vp9", "-crf", "30"])
        if include_audio:
            cmd.extend(["-c:a", "libopus", "-b:a", "128k"])
        else:
            cmd.append("-an")
    elif format_ext == "mkv":
        cmd.extend(["-c:v", "libx264", "-crf", "23"])
        if include_audio:
            cmd.extend(["-c:a", "aac", "-b:a", "128k"])
        else:
            cmd.append("-an")
    elif format_ext == "mov":
        cmd.extend(["-c:v", "libx264", "-preset", "medium"])
        if include_audio:
            cmd.extend(["-c:a", "aac", "-b:a", "128k"])
        else:
            cmd.append("-an")
    elif format_ext == "flv":
        cmd.extend(["-c:v", "flv"])
        if include_audio:
            cmd.extend(["-c:a", "mp3", "-b:a", "128k"])
        else:
            cmd.append("-an")
    else:
        if not include_audio:
            cmd.append("-an")
    
    cmd.append(output_path)
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    _, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{stderr}")
    return output_path

with col_center:
    if st.button("✨ Convert Video", type="primary"):
        if conversion_mode == "📥 YouTube Download" and not youtube_url:
            st.error("❌ Please enter a YouTube URL")
        elif conversion_mode == "📁 File Upload" and not uploaded_file:
            st.error("❌ Please upload a video file")
        else:
            try:
                with st.status("🔄 Converting video...", expanded=True) as status:
                    tmpdir = tempfile.mkdtemp(prefix="ytvid_")
                    
                    if conversion_mode == "📥 YouTube Download":
                        st.write("📥 Downloading YouTube video...")
                        input_file = download_youtube(youtube_url, tmpdir)
                        st.write(f"✅ Download complete: {os.path.basename(input_file)}")
                    else:
                        st.write("📥 Processing uploaded file...")
                        input_file = os.path.join(tmpdir, uploaded_file.name)
                        with open(input_file, "wb") as f:
                            f.write(uploaded_file.read())
                        st.write(f"✅ File uploaded: {uploaded_file.name}")
                    
                    st.write(f"🔄 Converting to {file_ext.upper()} format...")
                    output_path = os.path.join(tmpdir, output_filename)
                    
                    if format_option.startswith("AMV"):
                        convert_to_amv(
                            input_file, 
                            output_path,
                            width=width,
                            height=height,
                            fps=fps,
                            include_audio=include_audio
                        )
                    else:
                        convert_video(
                            input_file,
                            output_path,
                            file_ext,
                            width=width,
                            height=height,
                            fps=fps,
                            include_audio=include_audio
                        )
                    
                    st.write("✅ Conversion complete!")
                    status.update(label="✅ Conversion complete!", state="complete")
                    
                    with open(output_path, "rb") as f:
                        mime_types = {
                            "amv": "video/x-amv",
                            "mp4": "video/mp4",
                            "avi": "video/x-msvideo",
                            "mkv": "video/x-matroska",
                            "webm": "video/webm",
                            "mov": "video/quicktime",
                            "flv": "video/x-flv"
                        }
                        st.download_button(
                            label=f"⬇️ Download {file_ext.upper()} File",
                            data=f,
                            file_name=output_filename,
                            mime=mime_types.get(file_ext, "video/mp4")
                        )
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h3>📋 Supported Formats</h3>
        <p><strong>AMV:</strong> Low-resolution format for portable media players (160x120@12fps)</p>
        <p><strong>MP4:</strong> Most compatible format with H.264 codec</p>
        <p><strong>AVI:</strong> Classic format with MPEG-4 codec</p>
        <p><strong>MKV:</strong> High-quality Matroska container</p>
        <p><strong>WEBM:</strong> Web-optimized VP9 codec</p>
        <p><strong>MOV:</strong> QuickTime format</p>
        <p><strong>FLV:</strong> Flash video format</p>
        <p><strong>Custom:</strong> Set your own resolution, FPS, and codec settings</p>
        <br>
        <p><strong>Supported upload formats:</strong> MP4, AVI, MKV, MOV, WEBM, FLV, WMV, MPG, MPEG, 3GP, M4V, OGV, ASF, RM, RMVB, VOB, MTS, M2TS, DIVX, XVID, F4V, AMV, SWF, MPV, QT</p>
    </div>
    """, unsafe_allow_html=True)
