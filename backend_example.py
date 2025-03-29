"""
Example Flask backend for YouTube to Text Converter

This is a simple Flask application that provides an API endpoint
to download YouTube audio and convert it to text.

To use:
1. Install dependencies: pip install flask flask-cors yt-dlp speechrecognition
2. Run the server: python backend_example.py
3. Make requests to http://localhost:5000/api/convert with a YouTube URL
"""

import os
import subprocess
import tempfile
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def youtube_to_audio_yt_dlp(youtube_url, output_folder="."):
    """Downloads YouTube audio as MP3 and returns the file path."""
    os.makedirs(output_folder, exist_ok=True)
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", os.path.join(output_folder, "%(title)s.%(ext)s"),
        youtube_url
    ]
    
    try:
        print(f"Attempting to download: {youtube_url}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # Check stdout first
        output = result.stdout
        for line in output.splitlines():
            if "[ExtractAudio] Destination:" in line:
                return line.split("[ExtractAudio] Destination:", 1)[1].strip()
        
        # Check stderr if not found in stdout
        if not output:
            output = result.stderr
            for line in output.splitlines():
                if "[ExtractAudio] Destination:" in line:
                    return line.split("[ExtractAudio] Destination:", 1)[1].strip()
        
        # If still not found, try to find any .mp3 file in the output folder
        for file in os.listdir(output_folder):
            if file.endswith(".mp3"):
                return os.path.join(output_folder, file)
                
        raise Exception("Couldn't find MP3 file!")
    except subprocess.CalledProcessError as e:
        print(f"Download failed with error: {e.stderr}")
        raise Exception(f"Error downloading audio: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise Exception(f"Error processing video: {str(e)}")

def convert_mp3_to_text(mp3_file):
    """Converts an MP3 file to text using speech recognition."""
    recognizer = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(mp3_file) as source:
        audio_data = recognizer.record(source)
    
    # Use Google's speech recognition
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

@app.route('/api/convert', methods=['POST'])
def convert():
    # Get YouTube URL from request
    data = request.get_json()
    if not data or 'youtube_url' not in data:
        return jsonify({'error': 'YouTube URL is required'}), 400
    
    youtube_url = data['youtube_url']
    
    try:
        # Create a temporary directory for this request
        temp_dir = tempfile.mkdtemp()
        
        # Download YouTube audio
        mp3_file = youtube_to_audio_yt_dlp(youtube_url, temp_dir)
        
        # Convert audio to text
        # Note: For a real implementation, you might want to use a more
        # robust speech recognition service for better accuracy
        text = convert_mp3_to_text(mp3_file)
        
        # Clean up the temporary file
        os.remove(mp3_file)
        os.rmdir(temp_dir)
        
        return jsonify({
            'success': True,
            'text': text,
            'youtube_url': youtube_url
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 