# YouTube to Text Converter

This project provides a web interface to convert YouTube videos to text transcriptions. It consists of a frontend (HTML/CSS/JS) that can be hosted on GitHub Pages and requires a backend service to process the YouTube videos.

## Project Structure

- `index.html` - Main webpage with the user interface
- `styles.css` - Styling for the webpage
- `script.js` - Client-side JavaScript logic
- `README.md` - This documentation file

## Hosting on GitHub Pages

You can host the frontend part of this application on GitHub Pages for free:

1. Push this repository to GitHub
2. Go to the repository settings
3. Scroll down to the "GitHub Pages" section
4. Select the branch you want to publish (usually `main` or `master`)
5. Click "Save"
6. Your site will be published at `https://yourusername.github.io/repository-name/`

## Backend Requirements

GitHub Pages only hosts static content and cannot run server-side code. To make the YouTube to Text conversion work, you'll need to set up a separate backend service:

### Option 1: Create Your Own Backend

1. Set up a server using a free/low-cost service like:
   - [Heroku](https://www.heroku.com/) (has a free tier)
   - [Render](https://render.com/) (has a free tier)
   - [PythonAnywhere](https://www.pythonanywhere.com/) (has a free tier)
   - [AWS Lambda](https://aws.amazon.com/lambda/) (pay-per-use)

2. Deploy a backend service that:
   - Accepts YouTube URLs via an API endpoint
   - Uses the provided Python code to download YouTube audio
   - Converts the audio to text (you'll need to add speech recognition code)
   - Returns the text transcription

3. Update the `API_URL` in `script.js` to point to your backend service

### Python Code for Backend

The backend would use this Python code for downloading YouTube audio:

```python
import os
import subprocess

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
    
    # Get the list of mp3 files before download
    before_files = set([f for f in os.listdir(output_folder) if f.endswith('.mp3')])
    
    # Run the download command
    subprocess.run(command, check=True, capture_output=True, text=True)
    
    # Get the list of mp3 files after download
    after_files = set([f for f in os.listdir(output_folder) if f.endswith('.mp3')])
    
    # Find the new mp3 file(s)
    new_files = after_files - before_files
    
    if new_files:
        # Return the path to the new mp3 file
        new_file = list(new_files)[0]
        return os.path.join(output_folder, new_file)
    
    raise Exception("Couldn't find MP3 file!")
```

You would need to add speech recognition code to convert the MP3 to text (e.g., using Google's Speech-to-Text API, OpenAI's Whisper, or other services).

## Additional Backend Requirements

1. Install the necessary dependencies:
   - yt-dlp
   - A speech recognition library (e.g., SpeechRecognition, whisper)

2. Configure CORS to allow requests from your GitHub Pages domain

3. Set up proper error handling, rate limiting, and security measures

## Limitations

- Processing large videos may take significant time and resources
- Some videos may have copyright restrictions preventing downloads
- Speech recognition accuracy may vary depending on the video's audio quality

## License

MIT 