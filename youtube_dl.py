import pytube
from pytube import YouTube
from sys import argv
import os
import subprocess

link = argv[1]
yt = YouTube(link)

print("Title: " + yt.title)
print("Views: " + str(yt.views))
print("Duration: " + str(yt.length) + " seconds")
print("Author: " + yt.author)

choice = input(
    "Do you want to download the video (V) or extract the audio as an MP3 (A)? "
)

if choice.lower() == "v":
    # Download the video to the current directory
    video_stream = yt.streams.filter(progressive=True).first()
    if video_stream is not None:
        try:
            video_stream.download()
            print("Video downloaded successfully!")
        except Exception as e:
            print("An error occurred during video download.")
            print("Error details:", str(e))
    else:
        print("No video stream found.")
elif choice.lower() == "a":
    # Download the audio as a temporary file
    audio_streams = yt.streams.filter(only_audio=True)
    if audio_streams:
        # Sort audio streams in descending order of bitrate
        audio_streams = sorted(audio_streams, key=lambda s: s.abr, reverse=True)
        audio_stream = audio_streams[0]  # Select the highest quality audio stream
        try:
            temp_audio_path = audio_stream.download(filename="temp_audio")
            print("Audio extracted successfully!")
        except Exception as e:
            print("An error occurred during audio extraction.")
            print("Error details:", str(e))
    else:
        print("No audio stream found.")
else:
    print("Invalid choice. Please select 'V' for video or 'A' for audio.")

# Convert the temporary audio file to MP3 using ffmpeg
if choice.lower() == "a" and temp_audio_path:
    try:
        new_filename = f"{yt.title} ({yt.author}).mp3"
        new_audio_path = os.path.join(
            "/Users/joreal/Downloads/Thunderfunk", new_filename
        )
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                temp_audio_path,
                "-c:a",
                "libmp3lame",
                "-q:a",
                "0",
                new_audio_path,
            ]
        )
        print("Audio converted to MP3 successfully!")
        # Delete the temporary audio file
        os.remove(temp_audio_path)
    except Exception as e:
        print("An error occurred during audio conversion.")
        print("Error details:", str(e))
