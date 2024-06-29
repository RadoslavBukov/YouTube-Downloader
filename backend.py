"""
Downloads video and audio from a YouTube, with specific requirements about format, quality and length.

Function used:
    - find_url_by_name:
        input: author, title, api_key(provided from YouTube API)
        output: youtube_url (of provided inputs)
    - download_youtube_video:
        input: youtube_url, download_path, file_type, quality
        output: path (of downloaded file)
    - download_youtube_audio:
        input: youtube_url, download_path, file_type
        output: path (of downloaded file)
    - download_playlist:
        input: youtube_url, download_path, file_type
        output: path (of downloaded file)
    - trim_video:
        input: file_path, start_time(in sec), end_time(in sec)
        output: path (of trimmed file)
    - trim_audio:
        input: file_path, start_time(in sec), end_time(in sec)
        output: path (of trimmed file)
    - get_video_quality_options:
        input: youtube_url
        output: list ( with all existing resolutions of the video)
"""
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube, Playlist
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from googleapiclient.discovery import build
import os


# Find song in YouTube by Author and Title -> return video URL
def find_url_by_name(author, title, api_key):
    # Build the YouTube service
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Search for the video
    query = f"{title} {author}"
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=1
    )
    response = request.execute()

    # Extract the video URL from the response
    if 'items' in response and len(response['items']) > 0:
        video_id = response['items'][0]['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return None


# Download Video from url, in selected type with selected quality.
def download_youtube_video(youtube_url, download_path, file_type, quality):
    # Define the supported file types and their corresponding codecs
    supported_file_types = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']

    # Check if the provided file type is supported
    if file_type not in supported_file_types:
        raise ValueError("Unsupported file type for video. Supported types are 'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'.")

    # Create YouTube object
    yt = YouTube(youtube_url)

    # Select the video stream based on the desired quality
    video_stream = yt.streams.filter(type="video", res=quality).first()
    if not video_stream:
        raise ValueError(f"No streams available for quality: {quality}")

    # Download the video stream
    downloaded_file_path = video_stream.download(output_path=download_path)

    # Determine the base and new file path
    new_file = os.path.join(download_path, f"{yt.author} - {yt.title}({quality}).{file_type}")

    if file_type in supported_file_types:
        # Convert video to the desired format if needed
        if file_type != 'mp4':  # If not already in mp4 format, convert it
            video_clip = VideoFileClip(downloaded_file_path)
            video_clip.write_videofile(new_file, codec="libx264") # Specify codec for non-mp4 formats
            video_clip.close()
        else:
            # If already mp4, just rename the file
            os.rename(downloaded_file_path, new_file)
    else:
        raise ValueError("Unsupported file type for video. Supported types are 'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'.")

    # Remove the original downloaded file if it was converted or renamed
    if downloaded_file_path != new_file and os.path.exists(downloaded_file_path):
        os.remove(downloaded_file_path)

    return new_file


#TODO: Make it work with "m4r" format
def download_youtube_audio(youtube_url, download_path, file_type):
    # Define the supported file types and their corresponding codecs
    supported_file_types = {
        'mp3': 'libmp3lame',
        'wav': 'pcm_s16le',
        'aac': 'aac',
        'ogg': 'libvorbis',
        'flac': 'flac',
    }

    # Check if the provided file type is supported
    if file_type not in supported_file_types:
        raise ValueError(
            "Unsupported file type for audio. Supported types are 'mp3', 'wav', 'aac', 'ogg', 'flac'.")

    codec = supported_file_types[file_type]

    # Create YouTube object
    yt = YouTube(youtube_url)

    # Download the audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()
    downloaded_file_path = audio_stream.download(output_path=download_path)

    # Determine the base and new file path
    new_file = os.path.join(download_path, f"{yt.author} - {yt.title}.{file_type}")

    # Convert to audio format if needed
    audio = AudioFileClip(downloaded_file_path)
    audio.write_audiofile(new_file, codec=codec)
    audio.close()

    # Remove the original downloaded file
    os.remove(downloaded_file_path)

    return new_file


def download_playlist(url, download_path, file_type):
    pl = Playlist(url)
    downloaded_files = []

    for video_url in pl.video_urls:
        if file_type in ['mp3', 'wav', 'ogg', 'flac', 'm4r']:
            # Download audio if file_type is audio
            file = download_youtube_audio(video_url, download_path, file_type)
        elif file_type in ['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv']:
            # Download video if file_type is video
            file = download_youtube_video(video_url, download_path, file_type)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        downloaded_files.append(file)

    return downloaded_files



def trim_video(input_file, start_time, end_time):
    # Create a VideoFileClip object
    video_clip = VideoFileClip(input_file)

    # Define start and end times in seconds
    start_time_sec = start_time
    end_time_sec = end_time

    # Trim the video clip
    trimmed_clip = video_clip.subclip(start_time_sec, end_time_sec)

    # Determine the output file path
    input_filename, input_extension = os.path.splitext(input_file)
    output_file = f"{input_filename}_trimmed{input_extension}"

    # Export the trimmed video clip to a new file
    trimmed_clip.write_videofile(output_file, codec="libx264", audio_codec="aac")  # Adjust codecs as needed

    # Close the video clip objects
    video_clip.close()
    trimmed_clip.close()

    return output_file


def trim_audio(input_file, start_time, end_time):
    # Load the audio file
    audio_segment = AudioSegment.from_file(input_file)

    # Define start and end times in milliseconds
    start_time_ms = start_time * 1000
    end_time_ms = end_time * 1000

    # Trim the audio segment
    trimmed_segment = audio_segment[start_time_ms:end_time_ms]

    # Determine the output file path
    input_filename, input_extension = os.path.splitext(input_file)
    output_file = f"{input_filename}_trimmed{input_extension}"

    # Export the trimmed audio segment to a new file
    trimmed_segment.export(output_file, format=input_extension[1:])  # Adjust format as needed

    return output_file


def get_video_quality_options(youtube_url):
    yt = YouTube(youtube_url)

    # Get all streams (both video and audio)
    streams = yt.streams.filter(type="video")

    # Extract unique resolutions from the streams
    resolutions = []
    for stream in streams:
        if stream.resolution and stream.resolution not in resolutions:
            resolutions.append(stream.resolution)

    return resolutions


url = "https://www.youtube.com/watch?v=6Ejga4kJUts"
# api_key = "AIzaSyCl3cSv9YEpBVeIHiu0orL3qhZUqm_py6c"
# author = "BTR"
# title = "Spasenie"
# print(find_url_by_name(author, title, api_key))

# url = find_url_by_name(author, title)
download_pat = r"C:\Users\bukov\Downloads"
file_type = "mp4"
audio_file_path = r"C:\Users\bukov\Downloads\The Cranberries - Zombie.mp3"
video_file_path = r"C:\Users\bukov\Downloads\The Cranberries - Zombie.mp4"

# print(get_video_quality_options(url))
download_youtube_video(url, download_pat, file_type, "360p")
# download_youtube_audio(url, download_pat, file_type)
# trim_audio(audio_file_path, 95, 125)
# trim_video(video_file_path, 95, 125)