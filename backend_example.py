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
        # Get the list of mp3 files before download
        before_files = set([f for f in os.listdir(output_folder) if f.endswith('.mp3')])
        
        # Run the download command
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        # Get the list of mp3 files after download
        after_files = set([f for f in os.listdir(output_folder) if f.endswith('.mp3')])
        
        # Find the new mp3 file(s)
        new_files = after_files - before_files
        
        if new_files:
            # Return the path to the new mp3 file
            new_file = list(new_files)[0]
            return os.path.join(output_folder, new_file)
        
        raise Exception("Couldn't find MP3 file!")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error downloading audio: {e.stderr}")
    except Exception as e:
        raise Exception(f"Error processing video: {str(e)}")

def convert_mp3_to_text(mp3_file):
    """Converts an MP3 file to text using speech recognition."""
    recognizer = sr.Recognizer()
    
    try:
        # Load the audio file
        with sr.AudioFile(mp3_file) as source:
            audio_data = recognizer.record(source)
        
        # Use Google's speech recognition
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    except Exception as e:
        return f"Error processing audio: {str(e)}"

@app.route('/api/convert', methods=['POST'])
def convert():
    # Get YouTube URL from request
    data = request.get_json()
    if not data or 'youtube_url' not in data:
        return jsonify({
            'success': False,
            'error': 'YouTube URL is required'
        }), 400
    
    youtube_url = data['youtube_url']
    
    try:
        # Create a temporary directory for this request
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"Processing URL: {youtube_url}")
            
            # Download YouTube audio
            mp3_file = youtube_to_audio_yt_dlp(youtube_url, temp_dir)
            print(f"Downloaded audio: {mp3_file}")
            
            # Convert audio to text
            text = convert_mp3_to_text(mp3_file)
            print(f"Converted to text: {text[:100]}...")
            
            return jsonify({
                'success': True,
                'text': text,
                'youtube_url': youtube_url
            })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Backend is running'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 