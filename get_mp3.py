from pytube import YouTube
import os


def download_music(url, path):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=path)

    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print("target path = " + new_file)
    print("mp3 has been successfully downloaded.")
