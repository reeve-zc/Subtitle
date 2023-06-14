from yt_dlp import YoutubeDL

download_option = {'final_ext': 'mp3',
                   'format': 'bestaudio/best',
                   'postprocessors': [{'key': 'FFmpegExtractAudio',
                                       'nopostoverwrites': False,
                                       'preferredcodec': 'mp3',
                                       'preferredquality': '5'}],
                   'outtmpl': 'musics/%(title)s.%(ext)s'}

info_option = {'final_ext': 'mp3',
               'format': 'bestaudio/best',
               'writethumbnail': True,
               'postprocessors': [{
                   'format': 'jpg',
                   'key': 'FFmpegThumbnailsConvertor',
                   'when': 'before_dl'}],
               'skip_download': True,
               'outtmpl': 'temp/%(title)s.%(ext)s'}


def get_info(link):
    try:
        with YoutubeDL(info_option) as ydl:
            ydl.download(link)
            info_dict = ydl.extract_info(link, download=False)

            video_title = info_dict.get('title', None)
            video_duration = info_dict.get('duration_string', None)
            video_uploader = info_dict.get('uploader', None)
            return video_title, video_duration, video_uploader
    except:
        return False


def download_song(link):
    try:
        with YoutubeDL(download_option) as ydl:
            ydl.download(link)
    except:
        return "Download Failed"
