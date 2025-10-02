import os
import subprocess
import tempfile
import shutil
from yt_dlp import YoutubeDL

def download_youtube(url: str, download_dir: str) -> str:
    """
    Download the best available mp4 using yt-dlp and return path to file.
    """
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(download_dir, "%(title).200s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "yt_video")
        out_name = os.path.join(download_dir, f"{title}.mp4")
        ydl.params["outtmpl"] = os.path.join(download_dir, f"{title}.%(ext)s")
        ydl.download([url])

        # check for file in common formats
        for ext in ("mp4", "mkv", "webm"):
            candidate = os.path.join(download_dir, f"{title}.{ext}")
            if os.path.exists(candidate):
                return candidate
    raise FileNotFoundError("Downloaded file not found.")

def convert_to_amv(input_path: str, output_path: str,
                   width=160, height=120, fps=12,
                   v_bitrate="256k", audio_rate=22050, include_audio=True):
    """
    Convert a video to .amv using ffmpeg.
    """
    vcodec = "mpeg4"
    acodec = "mp2" if include_audio else "none"

    if include_audio:
        audio_args = ["-c:a", acodec, "-ar", str(audio_rate)]
    else:
        audio_args = ["-an"]

    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-vf", f"scale={width}:{height}",
        "-r", str(fps),
        "-b:v", v_bitrate,
        "-c:v", vcodec,
    ] + audio_args + [output_path]

    print("Running ffmpeg:", " ".join(cmd))
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    _, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{stderr}")
    return output_path

def youtube_to_amv(url: str, out_name: str = "output.amv"):
    tmpdir = tempfile.mkdtemp(prefix="ytamv_")
    try:
        print("Downloading YouTube video...")
        downloaded = download_youtube(url, tmpdir)
        print("Download complete:", downloaded)

        out_path = os.path.abspath(out_name)
        print("Converting to AMV...")
        convert_to_amv(downloaded, out_path)
        print("Done! Saved as", out_path)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

if __name__ == "__main__":
    # Example usage
    youtube_url = input("Paste YouTube URL: ")
    out_file = input("Output file name (example: myvideo.amv): ")
    if not out_file.endswith(".amv"):
        out_file += ".amv"
    youtube_to_amv(youtube_url, out_file)