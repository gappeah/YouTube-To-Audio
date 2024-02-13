import requests
from pytube import YouTube
import os
import moviepy
from pydub import AudioSegment
import re
import urllib.parse
from time import sleep


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

      # Downloading the audio stream
                audio_stream.download(output_path=os.getcwd(), filename=f"{title}.mp4")

                # Convert the downloaded audio to MP3
                audio = AudioSegment.from_file(audio_file, format='mp4')
                mp3_file = os.path.join(os.getcwd(), f"{title}.mp3")
                audio.export(mp3_file, format='mp3')

                # Clean up - remove the original MP4 audio file
                os.remove(audio_file)

                return mp3_file

            else:
                print(f"No audio stream found for {bitrate}kbps bitrate.")
                raise ValueError(f"No audio stream found")

    else:
        print("URL is not valid or does not belong to youtube.com")
        raise ValueError("Invalid URL or URL does not belong to youtube.com")

except Exception as e:
        print(f"An error occurred: {str(e)}")
