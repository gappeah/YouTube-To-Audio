import requests
from pytube import YouTube
import os
from pydub import AudioSegment
import re
import urllib.parse
from time import sleep

# Function to remove non-alphabet characters from the title.
def remove_non_alpha(s):
    return re.sub(r"[^a-zA-Z\s]", '', s).replace(' ', '-')

# Function to prompt for bitrate selection
def prompt_bitrate():
    print("Select the desired audio bitrate:")
    print("1. 32 kbps – generally acceptable only for speech")
    print("2. 96 kbps – generally used for speech or low-quality streaming")
    print("3. 128 kbps – mid-range bitrate quality")
    print("4. 192 kbps – medium-quality bitrate")
    print("5. 256 kbps – a commonly used high-quality bitrate")
    print("6. 320 kbps – highest level supported by the MP3 standard")
    
    bitrate_options = {
        "1": "32k",
        "2": "96k",
        "3": "128k",
        "4": "192k",
        "5": "256k",
        "6": "320k"
    }

    choice = input("Enter the number corresponding to your desired bitrate (1-6): ")
    return bitrate_options.get(choice, "320k")  # Default to 320 kbps if invalid input

# Validating input URL
try:
    video_url = input("Paste YouTube URL: ")
    result = urllib.parse.urlparse(video_url)

    # Check if the URL is valid and belongs to YouTube.com
    if result.scheme == "https" and (result.netloc == "www.youtube.com" or "youtu.be" in video_url):
        print("URL check... PASS")
        try:
            yt = YouTube(video_url)
        except:
            print("Failed to read URL. Retrying...")
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

            # Prompt for bitrate selection
            selected_bitrate = prompt_bitrate()
            print(f"Selected bitrate: {selected_bitrate}")

            # Downloading the audio stream
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_file = os.path.join(os.getcwd(), f"{title}.mp4")
            audio_stream.download(output_path=os.getcwd(), filename=f"{title}.mp4")

            # Convert the downloaded audio to MP3 with a sample rate of 48000
            audio = AudioSegment.from_file(os.path.abspath(audio_file), format='mp4')
            audio = audio.set_frame_rate(48000)  # Set sample rate to 48000
            mp3_file = os.path.join(os.getcwd(), f"{title}.mp3")
            audio.export(os.path.abspath(mp3_file), format='mp3', bitrate=selected_bitrate)
            
            # Clean up - remove the original MP4 audio file
            os.remove(audio_file)

            print("Audio conversion completed")
            print(f"MP3 file saved: {mp3_file}")

    else:
        print("URL is not valid or does not belong to youtube.com")
        raise ValueError("Invalid URL or URL does not belong to youtube.com")

except Exception as e:
    print(f"An error occurred: {str(e)}")