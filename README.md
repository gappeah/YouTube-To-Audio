
<<<<<<< HEAD
# YouTube-To-Audio

This Python script,  allows you to download audio from YouTube videos and convert them to MP3 format in 320 kbps.
=======
# YouTube-To-Audio (Work in Progress)

This Python script, although currently a work in progress, allows you to download audio from YouTube videos and convert them to MP3 format.
>>>>>>> 701195f87e0d98abb41775dbea30c182cb8331a6

**Features:**

* Validates YouTube video URLs.
* Extracts video title and removes non-alphabetical characters.
* Checks for video availability.
* Downloads the audio stream in MP4 format.
* Converts the MP4 audio to MP3 format.
* Cleans up by removing the downloaded MP4 file.

**Usage:**

1. Ensure you have the following libraries installed: `requests`, `pytube`, `os`, `pydub`, `re`, `urllib.parse`. You can install them using `pip install requests pytube os pydub re urllib.parse`.
<<<<<<< HEAD
2. Make sure you have FFmpeg installed on your system (https://github.com/BtbN/FFmpeg-Builds/releases) and the ffmpeg.exe, ffplay.exe, ffprobe.exe files in your project folder.
 Save the code as `youtube_mp3.py`.
=======
2. Save the code as `youtube_mp3.py`.
>>>>>>> 701195f87e0d98abb41775dbea30c182cb8331a6
3. Run the script: `python youtube_mp3.py`.
4. Paste the YouTube video URL when prompted.
5. The script will download the audio, convert it to MP3, and save it in the same directory as the script.

**Note:**
<<<<<<< HEAD
=======

>>>>>>> 701195f87e0d98abb41775dbea30c182cb8331a6
* This script is for educational purposes only and should not be used for downloading copyrighted material without permission.
* This is a work in progress and may have bugs or limitations.

**Next Steps:**

* Implement error handling for various scenarios.
* Add support for downloading different audio qualities.
* Allow users to specify the output directory for downloaded files.
* Consider adding a progress bar or other informational output during the download and conversion process.

I hope this information helps you understand and use the code!


