from yt_dlp import YoutubeDL

option = {'final_ext': 'mp3',
          'format': 'bestaudio/best',
          'postprocessors': [{'key': 'FFmpegExtractAudio',
                              'nopostoverwrites': False,
                              'preferredcodec': 'mp3',
                              'preferredquality': '5'}],
          'outtmpl': 'musics/%(title)s.%(ext)s'}


def get_info(link):
    try:
        with YoutubeDL(option) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_url = info_dict.get("url", None)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            return info_dict
    except:
        return False


def download_song(link):
    try:
        with YoutubeDL(option) as ydl:
            ydl.download(link)
    except:
        print("Download failed")


if __name__ == "__main__":
    url = "https://youtu.be/TUVcZfQe-Kw"
    download_song(url)
