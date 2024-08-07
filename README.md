# YouTube-To-Audio
![YouTube-to-Mp3](https://github.com/user-attachments/assets/625ae3b6-8d27-4710-9571-dbd4f38a6d4a)

A subset of the [YouTube Downloader](https://github.com/gappeah/YouTube-Downloader-Pro) script. This Python script allows you to download audio from YouTube videos and convert them to MP3 format in 32 kbit/s, 96 kbit/s, 128 kbit/s, 192 kbit/s, 256 kbit/s and 320 kbit/s

![image](https://github.com/user-attachments/assets/75a737b6-abe2-4374-8609-a5111e669e4c)


**Features:**

* Validates YouTube video URLs.
* Extracts video title and removes non-alphabetical characters.
* Checks for video availability.
* Downloads the audio stream in MP4 format.
* Converts the MP4 audio to MP3 format.
* Cleans up by removing the downloaded MP4 file.

**Usage:**
1. Ensure you have the following libraries installed: `requests`, `pytube`, `os`, `pydub`, `re`, `urllib.parse`. You can install them using `pip install requests pytube os pydub re urllib.parse`.
2. Make sure you have FFmpeg installed on your system (https://github.com/BtbN/FFmpeg-Builds/releases) and the ffmpeg.exe, ffplay.exe, ffprobe.exe files in your project folder.
3. Save the code as `youtube_mp3.py`.
4. Run the script: `python youtube_mp3.py`.
5. Paste the YouTube video URL when prompted.
6. The script will download the audio, convert it to MP3, and save it in the same directory as the script.

**Note:**
* This script is for educational purposes only and should not be used for downloading copyrighted material without permission.
* This is a work in progress and may have bugs or limitations.

**Updates:**
* Direct MP4 to MP3 conversion has been achieved.
* Both www.youtube.com or youtu.be are accepted.
* Added new standard sample rate 48 khz.
* Added new bitrate options 32 kbit/s – generally acceptable only for speech, 96 kbit/s – generally used for speech or low-quality streaming, 128 kbit/s – mid-range bitrate quality, 192 kbit/s – medium-quality bitrate, 256 kbit/s – a commonly used high-quality bitrate and 320 kbit/s – highest level supported by the MP3 standard.
