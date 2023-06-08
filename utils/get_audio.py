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

            video_title = info_dict.get('title', None)
            video_duration = info_dict.get('duration', None)
            video_uploader = info_dict.get('uploader', None)
            return video_title, video_duration, video_uploader
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
    get_info(url)
    download_song(url)
