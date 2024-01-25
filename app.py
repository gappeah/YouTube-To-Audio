import os
from moviepy.editor import AudioFileClip
from pytube import YouTube
import re
import urllib.parse
import requests
from time import sleep
from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
from pydub import AudioSegment

app = Flask(__name__)

# Function to remove non-alphabet characters from the title.
def remove_non_alpha(s):
    return re.sub(r"[^a-zA-Z\s]", '', s).replace(' ', '-')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            video_url = request.form['url']
            result = urllib.parse.urlparse(video_url)

            # Check if the URL is valid and belongs to YouTube.com
            if result.scheme == "https" and result.netloc == "www.youtube.com":
                print("URL check... PASS")
                try:
                    yt = YouTube(video_url)
                except:
                    print("Failed to read URL. Retrying...")
                    sleep(2)
                    yt = YouTube(video_url)

                raw_title = yt.title
                title = remove_non_alpha(raw_title)

                audio_bitrate = request.form['bitrate']
                audio_format = request.form['format']

                # Getting list of all available streams for input url.
                streams = yt.streams.filter(only_audio=True)
                bitrates = set(stream.abr for stream in streams if stream and stream.abr)
                formats = set(stream.mime_type.split('/')[1] for stream in streams if stream and stream.mime_type)

                download_bitrate = request.form['bitrate']
                download_format = request.form['format']

                file_name = f"{title}"
                output_dir = os.getcwd()

                selected_stream = yt.streams.filter(only_audio=True, abr=download_bitrate, mime_type=f'audio/{download_format}').first()

                if selected_stream:
                    print(f"Downloading audio stream with {download_bitrate} bitrate and {download_format} format...")
                    audio_file = os.path.join(output_dir, f"{file_name}.{download_format}")

                    # Downloading the audio stream
                    selected_stream.download(output_path=output_dir, filename=f"{file_name}.{download_format}")

                    # If the format is WAV, convert it to MP3
                    if download_format == 'wav':
                        audio = AudioSegment.from_wav(audio_file)
                        audio.export(os.path.join(output_dir, f"{file_name}.mp3"), format="mp3")
                        os.remove(audio_file)  # Remove the original WAV file
                        audio_file = os.path.join(output_dir, f"{file_name}.mp3")

                    return send_from_directory(directory=os.path.abspath(output_dir), filename=os.path.basename(audio_file), as_attachment=True)
                else:
                    print(f"No suitable audio stream found for {download_bitrate} bitrate and {download_format} format.")
                    raise ValueError(f"No suitable audio stream found")

            else:
                print("URL is not valid or does not belong to youtube.com")
                raise ValueError("Invalid URL or URL does not belong to youtube.com")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
