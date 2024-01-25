# YouTube to MP3 Converter

This is a simple web application that allows users to convert YouTube videos to MP3 audio files.

## Installation

1. Clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the app using `python app.py`.

## Usage

1. Open the web application in your browser.
2. Enter the URL of the YouTube video you want to convert.
3. Click the "Convert" button.
4. The converted MP3 audio file will be downloaded.

## Files

- `app.py`: Contains the main Flask application code.
- `index.html`: Contains the HTML template for the web page.

## Requirements

- Python 3
- Flask
- pytube
- moviepy

## Roadmap

- Add more features including:
    - Add more audio formats (MP3, FLAC, WAV)
    - Add more audio bitrate (128kbps, 192kbps, 320kbps)
    - Cleaner and friendly UI
    - Possibly swap the Pytube for the YoutubeDL or YouTube API for access the audio streams