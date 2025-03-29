import os
import subprocess
import tempfile
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr

app = Flask(__name__)
CORS(app)

def youtube_to_audio_yt_dlp(youtube_url, output_folder="."):
    os.makedirs(output_folder, exist_ok=True)
    command = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "mp3",
        "-o", os.path.join(output_folder, "%(title)s.%(ext)s"),
        youtube_url
    ]
    
    before_files = set([f for f in os.listdir(output_folder) if f.endswith('.mp3')])
    subprocess.run(command, check=True, capture_output=True, text=True)
    after_files = set([f for f in os.listdir(output_folder) if f.endswith('.mp3')])
    new_files = after_files - before_files
    
    if new_files:
        new_file = list(new_files)[0]
        return os.path.join(output_folder, new_file)
    raise Exception("Couldn't find MP3 file!")

def convert_mp3_to_text(mp3_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(mp3_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    if not data or 'youtube_url' not in data:
        return jsonify({'error': 'YouTube URL is required'}), 400
    
    youtube_url = data['youtube_url']
    try:
        temp_dir = tempfile.mkdtemp()
        mp3_file = youtube_to_audio_yt_dlp(youtube_url, temp_dir)
        text = convert_mp3_to_text(mp3_file)
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