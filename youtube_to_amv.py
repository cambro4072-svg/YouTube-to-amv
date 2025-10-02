import yt_dlp
import os

def download_and_convert(url, output_format="mp4"):
    try:
        # Output file name
        output_file = f"output.{output_format}"

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "temp.%(ext)s",
            "merge_output_format": output_format,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Rename to consistent output file
        for file in os.listdir("."):
            if file.startswith("temp."):
                os.rename(file, output_file)

        return output_file

    except Exception as e:
        print("Error:", e)
        return None
