from pytube import YouTube, Playlist
import moviepy.editor as mp
import os


def download_video(url, download_path, file_type, start_time=None, end_time=None):
    yt = YouTube(url)

    if file_type == 'mp3':
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=download_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    else:
        video = yt.streams.filter(file_extension=file_type).first()
        new_file = video.download(output_path=download_path)

    if start_time and end_time:
        clip = mp.VideoFileClip(new_file)
        clipped = clip.subclip(start_time, end_time)
        clipped.write_videofile(new_file, codec='libx264')

    return new_file


def download_playlist(url, download_path, file_type, start_time=None, end_time=None):
    pl = Playlist(url)
    downloaded_files = []
    for video_url in pl.video_urls:
        file = download_video(video_url, download_path, file_type, start_time, end_time)
        downloaded_files.append(file)
    return downloaded_files
