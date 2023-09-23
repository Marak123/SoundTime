# from dataclasses import dataclass

import yt_dlp
from yt_dlp.utils import DownloadError
from PIL import Image


from core.settings import OUTPUT_AUDIO_PATH, OUTPUT_TEMP_PATH, OUTPUT_IMAGE_PATH
from apis.song.tasks import adownload



class YouTube:
    id: str = "youtube"
    name: str = "YouTube"
    code: int = 1
    url_regex: str = (
                r'(https?://)?(www\.|music\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
            )


    """ self.ydl_opts = {
        # 'extract_flat': True,
        # 'force_generic_extractor': True,
        # 'extract_info': True,
        'format': 'bestaudio/best',  # Wybór najlepszej jakości audio
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Jeśli chcesz mp3 zamiast mp4
            'preferredquality': '192',  # Jakość audio
        }],
        # 'postprocessor_args': [
        #     '-acodec', 'libmp3lame',
        #     '-ar', '44100',
        # ],
        # 'force_generic_extractor': True,
        # 'outtmpl': '%(id)s.%(ext)s',  # Nazwa pliku
        # 'download_archive': 'downloaded.txt',  # Plik śledzenia pobranych plików
        # 'quiet': False,  # Wyłączanie logów
        # 'extractor_args': {
        #     'youtube': {
        #         'get_comments': False,  # Wyłączenie pobierania komentarzy
        #     },
        # },
        # 'force_generic_extractor': True,
        # 'force_generic_format': True,
        # 'force_generic_extractors': True,
        # 'force_generic_formats': True,
        # 'force_generic_protocol': True,
        # 'force_generic_downloader': True,
        # 'youtube_include_dash_manifest': False,  # Wyłączenie manifestu DASH
        # 'skip_download': True,  # Pomijanie faktycznego pobierania plików,
        'progress_hooks': [YouTubeMedia.progress_hooks],
        'paths': {
            'home': YouTubeMedia.outputPathSong,
            'temp': YouTubeMedia.outputPathTemp,
        },
        # 'outtmpl': '%(id)s/%(id)s.%(ext)s',
        'writethumbnail': True,
        'quiet': True,
    } """


    @classmethod
    def info(self, url: str) -> dict:
        opts = {
            'format': 'bestaudio/best',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)

    @classmethod
    def download(self, url: str, uuidName: str) -> str:
        adownload.delay(
            url=url,
            objectId=uuidName,
            thumbnail_outputDir=f'{OUTPUT_IMAGE_PATH}{uuidName}/',
            outputSongPathTemplate=f'{uuidName}.%(ext)s'
        )
