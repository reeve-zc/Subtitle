from yt_dlp import YoutubeDL


option = {'final_ext': 'mp3',
          'format': 'bestaudio/best',
          'postprocessors': [{'key': 'FFmpegExtractAudio',
                              'nopostoverwrites': False,
                              'preferredcodec': 'mp3',
                              'preferredquality': '5'}],
          'outtmpl': 'musics/%(title)s.%(ext)s'}


def download_song(link):
    try:
        with YoutubeDL(option) as ydl:
            ydl.download([link])
    except:
        print("Download failed.")


if __name__ == "__main__":
    url = "https://youtu.be/TUVcZfQe-Kw"
    download_song(url)
