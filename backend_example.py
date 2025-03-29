"""
Example Flask backend for YouTube to Text Converter

This is a simple Flask application that provides an API endpoint
to download YouTube audio and convert it to text.

To use:
1. Install dependencies: pip install flask flask-cors pytube speechrecognition
2. Run the server: python backend_example.py
3. Make requests to http://localhost:5000/api/convert with a YouTube URL
"""

import os
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
        print(f"Attempting to download: {youtube_url}")
        
        # Create a YouTube object
        yt = YouTube(youtube_url)
        
        # Get the audio stream (highest quality)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        if not audio_stream:
            raise Exception("No audio stream found")
            
        # Download the audio
        print(f"Downloading audio stream: {audio_stream.itag}")
        output_file = audio_stream.download(output_path=output_folder)
        
        print(f"Downloaded to: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Download failed with error: {str(e)}")
        raise Exception(f"Error downloading audio: {str(e)}")

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
        
        # Download YouTube audio
        audio_file = youtube_to_audio_pytube(youtube_url, temp_dir)
        
        # Convert audio to text
        text = convert_audio_to_text(audio_file)
        
        # Clean up the temporary file
        os.remove(audio_file)
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