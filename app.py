import os
from moviepy.editor import AudioFileClip
from pytube import YouTube
import re
import urllib.parse
import requests
from time import sleep
import flask

# Function to remove non-alphabet characters from the title.
def remove_non_alpha(s):
    return re.sub(r"[^a-zA-Z\s]", '', s).replace(' ', '-')

# Validating input url
try:
    video_url = input("Paste YouTube URL: ")
    result = urllib.parse.urlparse(video_url)

    # Check if the URL is valid and belongs to YouTube.com
    if result.scheme == "https" and result.netloc == "www.youtube.com":
        print("URL check... PASS")
        try:
            yt = YouTube(video_url)
        except:
            print("Failed to read url. Retrying...")
            sleep(2)
            yt = YouTube(video_url)
        raw_title = yt.title
        title = remove_non_alpha(raw_title)

        # Send a request to the URL and check if the video is available
        response = requests.get(video_url)
        if "Video unavailable" in response.text:
            print("Video is not available on YouTube")
            raise ValueError("Video is not available on YouTube")
        else:
            print(f"Title: {title}")
            print("Gathering available streams...")
            sleep(2)

    else:
        print("URL is not valid or does not belong to youtube.com")
        raise ValueError("Invalid URL or URL does not belong to youtube.com")

    # Audio bitrate for 'audio_only' and merging video/audio above 1080p. Bitrate 160kbps can also be used for 2K and 4K videos.
    audio_bitrate = '128kbps'

    # This condition only handles downloading and uploading of audio-only file
    if download_quality == 'audio':
        audio_only = yt.streams.filter(abr=audio_bitrate).first()
        print("Downloading audio-only file...")
        audio_file = os.path.join(output_dir, f"{file_name}.m4a")
        audio_only.download(output_path=output_dir, filename=f"{file_name}.m4a")
        #audio_only.download() #(output_path=output_dir, filename=f"{file_name}.m4a")


except Exception as e:
    print(f"An error occurred: {str(e)}")
