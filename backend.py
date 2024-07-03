r"""
Downloads video and audio from a YouTube, with specific requirements about format, quality and length.

Function used:
    - find_url_by_name:
        input: author, title
            *need also api_key(provided from YouTube API) - Included in r"static_file\ setup.json" with key = "api_key"
        output: youtube_url (of provided inputs)
    - download_youtube_video:
        input: youtube_url, download_path, file_type, quality, start_time, end_time
        output: path (of downloaded file)
    - download_youtube_audio:
        input: youtube_url, download_path, file_type, quality, start_time, end_time
        output: path (of downloaded file)
    - download_playlist:
        input: youtube_url, download_path, file_type, quality, start_time, end_time
        output: path (of downloaded files)
    - trim_video:
        input: file_path, start_time(in sec), end_time(in sec)
        output: path (of trimmed file)
    - trim_audio:
        input: file_path, start_time(in sec), end_time(in sec)
        output: path (of trimmed file)
    - get_video_quality_options:
        input: youtube_url
        output: list ( with all existing resolutions of the video)
    - extract_thumbnail_from_url:
        input: url
        output: image data
    - get_value_from_json(key):
        {key: value}
        input: data key from the setup.json
        output: value linked to this key
    - time_to_seconds(time_str):
        input: time in format - min:sec (00:00)
        output: sum of minutes
        example: input(1:30) -> output (90) sec

Work as console app:
    python backend.py <"youtube_url" or "Artist Name"> <download_path> type --quality <quality> --start <start_time> --end <end_time>
        types are:
            - audio
            - vide
            - play list
        quality, start_time, end_time have default_values = ""

    Examples:
        - Download audio(mp3) by Artist and Name:
            python backend.py audio "The Cranberries" "Zombie" "C:\Users\name\Downloads" "mp3"
        - Download vide(mp4) by url
            python backend.py video "https://www.youtube.com/watch?v=6Ejga4kJUts" "C:\Users\name\Downloads" "mp4"
"""

import json
from io import BytesIO
import requests
from PIL import Image
# from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import VideoFileClip, AudioFileClip
from proglog import ProgressBarLogger
from pytube import YouTube, Playlist
from pydub import AudioSegment
from moviepy.editor import VideoFileClip
from googleapiclient.discovery import build
import os
import sys
import argparse # Work with console


# Find song in YouTube by Author and Title -> return video URL
def find_url_by_name(author, title):
    api_key = get_value_from_json("api_key")
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
def download_youtube_video(youtube_url, download_path, media_type, quality, start_time='', end_time='', logger=None):
    # Define the supported file types and their corresponding codecs
    supported_video_file_types = get_value_from_json("supported_video_file_types")

    # Check if the provided file type is supported
    if media_type not in supported_video_file_types:
        raise ValueError("Unsupported file type for video.")

    # Create YouTube object
    try:
        yt = YouTube(youtube_url)
    except Exception as e:
        return f"Invalid YouTube URL: {str(e)}"

    # Select the video stream based on the desired quality
    if quality == "":
        video_stream = yt.streams.get_highest_resolution()
        quality = video_stream.resolution
    else:
        video_stream = yt.streams.filter(type="video", res=quality).order_by("resolution").first()

    if not video_stream:
        raise ValueError(f"No streams available for quality: {quality}")

    # Download the video stream
    downloaded_file_path = video_stream.download(output_path=download_path)

    # Determine the base and new file path
    new_file = os.path.join(download_path, f"{yt.author} - {yt.title}({quality}).{media_type}")

    if media_type in supported_video_file_types:
        # Convert video to the desired format if needed
        if media_type != 'mp4':  # If not already in mp4 format, convert it
            video_clip = VideoFileClip(downloaded_file_path)
            video_clip.write_videofile(new_file, codec="libx264", logger=logger)  # Specify codec for non-mp4 formats
            video_clip.close()
        else:
            # If already mp4, just rename the file
            os.rename(downloaded_file_path, new_file)
    else:
        raise ValueError(
            f"Unsupported file type for video. Supported types are {', '.join(supported_video_file_types)}.")

    if not video_stream.includes_audio_track:
        # Download the audio stream
        audio_file = download_youtube_audio(youtube_url, download_path, "mp3")
        new_file = merge_video_and_audio_file(new_file, audio_file)

    # Remove the original downloaded file if it was converted or renamed
    if downloaded_file_path != new_file and os.path.exists(downloaded_file_path):
        os.remove(downloaded_file_path)

    if start_time != "" or end_time != "":
        if start_time == "":
            start_time = "00:00"
        if end_time == "":
            end_time = yt.length

        start_time_seconds = time_to_seconds(start_time)
        end_time_seconds = yt.length if end_time == yt.length else time_to_seconds(end_time)

        trimed_file = trim_video(new_file, start_time_seconds, end_time_seconds)
        os.remove(new_file)
        return trimed_file
    else:
        return new_file


# TODO: Make it work with "m4r" format
def download_youtube_audio(youtube_url, download_path, media_type, start_time='', end_time=''):
    # Define the supported file types and their corresponding codecs
    supported_audio_file_types_dict = get_value_from_json("supported_audio_file_types")
    supported_audio_file_types = list(supported_audio_file_types_dict.keys())

    # Check if the provided file type is supported
    if media_type not in supported_audio_file_types:
        raise ValueError(
            f"Unsupported file type for audio. Supported types are {', '.join(supported_audio_file_types)}.")

    codec = supported_audio_file_types_dict[media_type]

    # Create YouTube object
    try:
        yt = YouTube(youtube_url)
    except Exception as e:
        return f"Invalid YouTube URL: {str(e)}"

    # Download the best quality audio stream
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    downloaded_file_path = audio_stream.download(output_path=download_path)

    # Determine the base and new file path
    new_file = os.path.join(download_path, f"{yt.author} - {yt.title}.{media_type}")

    # Convert to audio format if needed
    audio = AudioFileClip(downloaded_file_path)
    audio.write_audiofile(new_file, codec=codec)
    audio.close()

    # Remove the original downloaded file
    os.remove(downloaded_file_path)

    if start_time != "" or end_time != "":
        if start_time == "":
            start_time = "00:00"
        if end_time == "":
            end_time = yt.length

        start_time_seconds = time_to_seconds(start_time)
        end_time_seconds = yt.length if end_time == yt.length else time_to_seconds(end_time)

        trimed_file = trim_audio(new_file, start_time_seconds, end_time_seconds)
        os.remove(new_file)
        return trimed_file
    else:
        return new_file


def download_playlist(playlist_url, download_path, media_type, quality, start_time, end_time):
    pl = Playlist(playlist_url)
    downloaded_files = []
    supported_audio_file_types_dict = get_value_from_json("supported_audio_file_types")
    supported_audio_file_types = list(supported_audio_file_types_dict.keys())
    supported_video_file_types = get_value_from_json("supported_video_file_types")

    for video_url in pl.video_urls:
        if media_type in supported_video_file_types:
            # Download audio if file_type is audio
            file = download_youtube_audio(video_url, download_path, media_type, start_time, end_time)
        elif media_type in supported_video_file_types:
            # Download video if file_type is video
            file = download_youtube_video(video_url, download_path, media_type, quality, start_time, end_time)
        else:
            raise ValueError(f"Unsupported file type: {media_type}")

        downloaded_files.append(file)

    return downloaded_files


def merge_video_and_audio_file(video_file_path, audio_file_path):
    try:
        video = VideoFileClip(video_file_path)
        if video is None:
            raise ValueError(f"Failed to load video from {video_file_path}")

        audio = AudioFileClip(audio_file_path)
        if audio is None:
            raise ValueError(f"Failed to load audio from {audio_file_path}")

        # Set the audio of the video clip
        final_video = video.set_audio(audio)

        # Write the merged file to the original video file path
        merged_file_path = video_file_path.replace(".mp4", "_m.mp4")
        final_video.write_videofile(merged_file_path, codec="libx264", audio_codec="aac")

        audio.close()
        video.close()
        os.remove(video_file_path)
        os.remove(audio_file_path)
        return final_video

    except Exception as e:
        print(f"Error merging video and audio: {e}")
        return None

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
    trimmed_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", logger=logger)

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
    trimmed_segment.export(output_file, format=input_extension[1:])

    return output_file


def get_video_name(youtube_url):
    yt = YouTube(youtube_url)
    author = yt.author
    title = yt.title
    name = f"{author} - {title}"
    if len(name) > 30:
        name = f"{author[:10]} - {title[:20]}" + "..." # Slice author and title separately
    return name

def get_video_time(youtube_url):
    try:
        yt = YouTube(youtube_url)
        length_seconds = yt.length
        minutes = length_seconds // 60
        seconds = length_seconds % 60
        return f"{minutes}:{seconds:02}"  # format as min:sec
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_video_quality_options(youtube_url):
    yt = YouTube(youtube_url)

    # Get all streams (both video and audio)
    streams = yt.streams.filter(type="video").order_by('resolution').asc()

    # Extract unique resolutions from the streams
    resolutions = []
    for stream in streams:
        if stream.resolution and stream.resolution not in resolutions:
            resolutions.append(stream.resolution)

    return resolutions


def extract_thumbnail_from_url(img_url):
    max_width = 500
    max_height = 300

    yt = YouTube(img_url)
    thumbnail_url = yt.thumbnail_url
    # Split the URL at the '?' character
    thumbnail_jpg_url = thumbnail_url.split('?')[0]

    response = requests.get(thumbnail_jpg_url)
    img_data = response.content
    image = Image.open(BytesIO(img_data))
    image.thumbnail((max_width, max_height))
    return image


def get_value_from_json(key_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Directory of the current script
    file_path = os.path.join(script_dir, 'static_files', 'setup.json')  # Corrected file path with proper path separator

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            if isinstance(data, list) and len(data) > 0:
                first_entry = data[0]
                if key_name in first_entry:
                    return first_entry[key_name]
                else:
                    raise KeyError(f'Key "{key_name}" not found in JSON data')
            else:
                raise ValueError('Invalid JSON format or empty data')
    except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError) as e:
        print(f'Error: {e}')
        return None


def time_to_seconds(time_str):
    try:
        minutes, seconds = map(int, time_str.split(':'))
        total_minutes = minutes*60 + seconds
        return total_minutes
    except ValueError:
        raise ValueError("Invalid time format. Please use 'min:sec' format.")


class MyBarLogger(ProgressBarLogger):

    def __init__(self):
        super().__init__()
        self.last_message = ''
        self.previous_percentage = 0

    def callback(self, **changes):
        # Every time the logger message is updated, this function is called with
        # the `changes` dictionary of the form `parameter: new value`.
        for (parameter, value) in changes.items():
            # print ('Parameter %s is now %s' % (parameter, value))
            self.last_message = value

    def bars_callback(self, bar, attr, value, old_value=None):
        # Every time the logger progress is updated, this function is called
        if 'Writing video' in self.last_message:
            percentage = (value / self.bars[bar]['total']) * 100
            if percentage > 0 and percentage < 100:
                if int(percentage) != self.previous_percentage:
                    self.previous_percentage = int(percentage)
                    print(self.previous_percentage)

# def console_app():
#     parser = argparse.ArgumentParser(description='YouTube Downloader and Converter')
#     parser.add_argument('action', choices=['video', 'audio', 'playlist'], help='Action to perform')
#     parser.add_argument('url_or_author', help='YouTube URL, author, or playlist URL')
#     parser.add_argument('title', nargs='?', default=None, help='Title of the video (optional, if author is provided)')
#     parser.add_argument('download_path', help='Path to download the files')
#     parser.add_argument('media_type', choices=['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'mp3', 'wav', 'aac', 'ogg', 'flac', 'm4r'], default='mp3', help='Media type (default: mp3)')
#     parser.add_argument('--quality', default="", help='Quality of video (e.g., 720p)')
#     parser.add_argument('--start_time', default="", help='Start time for trimming (format: min:sec)')
#     parser.add_argument('--end_time', default="", help='End time for trimming (format: min:sec)')
#     args = parser.parse_args()
#
#     # Debug Print: Print all arguments received
#     print("Received Arguments:")
#     print(f"- Action: {args.action}")
#     print(f"- URL or Author: {args.url_or_author}")
#     if args.title:
#         print(f"- Title: {args.title}")
#     print(f"- Download Path: {args.download_path}")
#     print(f"- Media Type: {args.media_type}")
#     print(f"- Quality: {args.quality}")
#     print(f"- Start Time: {args.start_time}")
#     print(f"- End Time: {args.end_time}")
#
#     # Determine if the provided url_or_author is a URL or author + title
#     if args.title:
#         # Assume url_or_author is the author and title is provided
#         youtube_url = find_url_by_name(args.url_or_author, args.title)
#         if not youtube_url:
#             print("Error: Could not find video for the given author and title.")
#             return
#     else:
#         # Assume url_or_author is the actual URL
#         youtube_url = args.url_or_author
#
#     if args.action == 'video':
#         try:
#             download_youtube_video(youtube_url, args.download_path, args.media_type, args.quality, args.start_time, args.end_time)
#             print(f"Video downloaded successfully to {args.download_path}")
#         except Exception as e:
#             print(f"Error downloading video: {str(e)}")
#     elif args.action == 'audio':
#         try:
#             download_youtube_audio(youtube_url, args.download_path, args.media_type, args.start_time, args.end_time)
#             print(f"Audio downloaded successfully to {args.download_path}")
#         except Exception as e:
#             print(f"Error downloading audio: {str(e)}")
#     elif args.action == 'playlist':
#         try:
#             download_playlist(youtube_url, args.download_path, args.media_type, args.quality, args.start_time, args.end_time)
#             print(f"Playlist downloaded successfully to {args.download_path}")
#         except Exception as e:
#             print(f"Error downloading playlist: {str(e)}")
#
#
# if __name__ == "__main__":
#     console_app()



# SECTION: Tests
# Console App Tests
# python backend.py audio https://www.youtube.com/watch?v=6Ejga4kJUts "C:\Users\bukov\Downloads" "mp3"
# python youtube_downloader.py <youtube_url> <download_path> audio --quality <quality> --start <start_time> --end <end_time>
# python backend.py audio "The Cranberries" "Zombie" "C:\Users\bukov\Downloads" "mp3"


# Function Tests
if __name__ == "__main__":
    # url = "https://www.youtube.com/watch?v=6Ejga4kJUts"
    # api_key = "AIzaSyCl3cSv9YEpBVeIHiu0orL3qhZUqm_py6c"
    url = "https://www.youtube.com/watch?v=WDaNJW_jEBo"

    # author = "BTR"
    # title = "Spasenie"
    # print(find_url_by_name(author, title, api_key))
    #
    # url = find_url_by_name(author, title)
    download_path = r"C:\Users\bukov\Downloads\Music"
    # audio_file_path = r"C:\Users\bukov\Downloads\The Cranberries - Zombie.mp3"
    # video_file_path = r"C:\Users\bukov\Downloads\The Cranberries - Zombie.mp4"
    #
    # download_youtube_video(url, download_pat, "mp4", "720p", "", "")
    download_youtube_audio(url, download_path, "mp3", "00:32", "")
    # trim_audio(audio_file_path, 95, 125)
    # trim_video(video_file_path, 95, 125)
    # print(extract_thumbnail_from_url(url))
    # print(get_value_from_json("supported_video_file_types"))
    # print(find_url_by_name("BTR", "Spasenie"))
    # print(get_video_name(url))
    # print(get_video_quality_options(url))