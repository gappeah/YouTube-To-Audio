import requests
from pytube import YouTube
import os
from pydub import AudioSegment
import re
import urllib.parse
from time import sleep
import zipfile
import shutil
from io import BytesIO

# URL for the ffmpeg zip file from GitHub
FFMPEG_ZIP_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

# Function to download and extract ffmpeg executables
# Function to find the bin folder dynamically after extraction
def find_bin_folder(root_dir):
    for root, dirs, files in os.walk(root_dir):
        if 'bin' in dirs:
            return os.path.join(root, 'bin')
    return None

# Function to download and extract ffmpeg executables
def download_and_extract_ffmpeg():
    # Directory where ffmpeg will be extracted
    ffmpeg_dir = os.path.join(os.getcwd(), 'ffmpeg-master-latest-win64-gpl')
    project_dir = os.getcwd()  # Your main project directory (YouTube-To-Audio folder)

    # Define the final paths of the executables in the project directory
    ffmpeg_exe = os.path.join(project_dir, 'ffmpeg.exe')
    ffprobe_exe = os.path.join(project_dir, 'ffprobe.exe')
    ffplay_exe = os.path.join(project_dir, 'ffplay.exe')

    # Check if ffmpeg executables are already present in the project directory
    if os.path.exists(ffmpeg_exe) and os.path.exists(ffprobe_exe) and os.path.exists(ffplay_exe):
        print("ffmpeg executables already downloaded and extracted.")
        return  # Exit the function as no further action is needed

    try:
        print("Downloading ffmpeg...")
        response = requests.get(FFMPEG_ZIP_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Create a directory to extract ffmpeg if it doesn't exist
        if not os.path.exists(ffmpeg_dir):
            os.makedirs(ffmpeg_dir)

        # Extract the zip file into the ffmpeg directory
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(ffmpeg_dir)

        print("ffmpeg download and extraction completed.")

        # Find the bin directory dynamically (recursively search)
        ffmpeg_bin_dir = find_bin_folder(ffmpeg_dir)

        if ffmpeg_bin_dir is None:
            raise FileNotFoundError("Bin folder not found after extraction")

        print(f"Extracted contents in bin folder: {os.listdir(ffmpeg_bin_dir)}")  # Debug: Check if the bin folder exists

        # Move the executables from 'bin' to the project folder
        if os.path.exists(os.path.join(ffmpeg_bin_dir, 'ffmpeg.exe')):
            shutil.move(os.path.join(ffmpeg_bin_dir, 'ffmpeg.exe'), ffmpeg_exe)
            print("Moved ffmpeg.exe")
        else:
            print("ffmpeg.exe not found!")

        if os.path.exists(os.path.join(ffmpeg_bin_dir, 'ffprobe.exe')):
            shutil.move(os.path.join(ffmpeg_bin_dir, 'ffprobe.exe'), ffprobe_exe)
            print("Moved ffprobe.exe")
        else:
            print("ffprobe.exe not found!")

        if os.path.exists(os.path.join(ffmpeg_bin_dir, 'ffplay.exe')):
            shutil.move(os.path.join(ffmpeg_bin_dir, 'ffplay.exe'), ffplay_exe)
            print("Moved ffplay.exe")
        else:
            print("ffplay.exe not found!")

        # Delete the extracted ffmpeg folder after moving the necessary files
        shutil.rmtree(ffmpeg_dir)
        print("Cleaned up the ffmpeg directory.")

    except Exception as e:
        print(f"Error during ffmpeg download or extraction: {str(e)}")
        raise

# Call this function at the beginning of your script
download_and_extract_ffmpeg()

# Set the path to ffmpeg in pydub
AudioSegment.converter = os.path.join(os.getcwd(), "ffmpeg.exe")

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