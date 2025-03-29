"""
Example Flask backend for YouTube to Text Converter

This is a simple Flask application that provides an API endpoint
to download YouTube audio and convert it to text.

To use:
1. Install dependencies: pip install flask flask-cors pytube yt-dlp speechrecognition
2. Run the server: python backend_example.py
3. Make requests to http://localhost:5000/api/convert with a YouTube URL
"""

import os
import subprocess
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
from pytube import YouTube

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def youtube_to_audio_pytube(youtube_url, output_folder="."):
    """Downloads YouTube audio using pytube and returns the file path."""
    try:
        print(f"[pytube] Attempting to download: {youtube_url}")
        
        # Create a YouTube object with custom parameters
        yt = YouTube(youtube_url, use_oauth=False, allow_oauth_cache=False)
        
        # Get the audio stream (highest quality)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not audio_stream:
            raise Exception("No audio stream found")
            
        # Download the audio
        print(f"[pytube] Downloading audio stream: {audio_stream.itag}")
        output_file = audio_stream.download(output_path=output_folder)
        
        print(f"[pytube] Downloaded to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"[pytube] Download failed with error: {str(e)}")
        raise Exception(f"Pytube download failed: {str(e)}")

def youtube_to_audio_yt_dlp(youtube_url, output_folder="."):
    """Fallback method using yt-dlp when pytube fails."""
    try:
        print(f"[yt-dlp] Attempting to download: {youtube_url}")
        
        # Prepare the output template
        output_template = os.path.join(output_folder, "%(title)s.%(ext)s")
        
        # Configure yt-dlp command
        command = [
            "yt-dlp",
            "--no-playlist",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--no-warnings",
            "--quiet",
            "-o", output_template,
            youtube_url
        ]
        
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"yt-dlp error: {result.stderr}")
            
        # Find the output file
        for file in os.listdir(output_folder):
            if file.endswith(".mp3"):
                output_file = os.path.join(output_folder, file)
                print(f"[yt-dlp] Downloaded to: {output_file}")
                return output_file
                
        raise Exception("Could not find downloaded file")
        
    except Exception as e:
        print(f"[yt-dlp] Download failed with error: {str(e)}")
        raise Exception(f"yt-dlp download failed: {str(e)}")

def download_audio(youtube_url, output_folder="."):
    """Try downloading with pytube first, fall back to yt-dlp if it fails."""
    try:
        return youtube_to_audio_pytube(youtube_url, output_folder)
    except Exception as pytube_error:
        print(f"Pytube failed, trying yt-dlp. Error was: {str(pytube_error)}")
        try:
            return youtube_to_audio_yt_dlp(youtube_url, output_folder)
        except Exception as yt_dlp_error:
            raise Exception(f"All download methods failed. Pytube error: {str(pytube_error)}. yt-dlp error: {str(yt_dlp_error)}")

def convert_audio_to_text(audio_file):
    """Converts an audio file to text using speech recognition."""
    recognizer = sr.Recognizer()
    
    # Load the audio file
    with sr.AudioFile(audio_file) as source:
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
        print(f"Created temporary directory: {temp_dir}")
        
        # Download YouTube audio with fallback
        audio_file = download_audio(youtube_url, temp_dir)
        
        # Convert audio to text
        text = convert_audio_to_text(audio_file)
        
        # Clean up the temporary file
        os.remove(audio_file)
        os.rmdir(temp_dir)
        print("Cleaned up temporary files")
        
        return jsonify({
            'success': True,
            'text': text,
            'youtube_url': youtube_url
        })
    
    except Exception as e:
        print(f"Error in convert endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True) 