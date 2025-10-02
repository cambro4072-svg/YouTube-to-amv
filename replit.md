# Video Converter Pro

## Overview
A professional video converter application that allows users to download YouTube videos and convert them to various formats, or upload their own video files for conversion.

## Features
- **YouTube Download**: Download and convert YouTube videos
- **File Upload**: Upload video files in 25+ formats for conversion
- **Multiple Output Formats**: AMV, MP4, AVI, MKV, WEBM, MOV, FLV, and custom settings
- **Custom Settings**: Adjust resolution, FPS, and audio settings
- **Modern UI**: Beautiful gradient design with responsive layout

## Tech Stack
- **Frontend**: Streamlit (running on port 5000)
- **Backend**: Python 3.11
- **Video Processing**: FFmpeg, yt-dlp
- **Dependencies**: streamlit, yt-dlp, tqdm

## Supported Input Formats
MP4, AVI, MKV, MOV, WEBM, FLV, WMV, MPG, MPEG, 3GP, M4V, OGV, ASF, RM, RMVB, VOB, MTS, M2TS, DIVX, XVID, F4V, AMV, SWF, MPV, QT

## Project Structure
- `streamlit_app.py` - Main Streamlit web application
- `youtube_to_amv.py` - Core conversion logic and YouTube download functions
- `requirements.txt` - Python dependencies
- `.streamlit/config.toml` - Streamlit configuration for Replit environment

## Recent Changes (October 2, 2025)
- Imported from GitHub and configured for Replit environment
- Added file upload functionality alongside YouTube download
- Expanded supported formats to 25+ video file types
- Redesigned UI with modern gradient theme and enhanced aesthetics
- Configured Streamlit to work with Replit's proxy setup (port 5000, 0.0.0.0 host)
- Set up deployment configuration for autoscale

## Configuration
The app is configured to:
- Run on port 5000 with host 0.0.0.0
- Disable CORS and XSRF protection for Replit proxy
- Use autoscale deployment target
