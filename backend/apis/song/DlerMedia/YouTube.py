from pytube import YouTube
import requests, os, re, yt_dlp, json

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.conf import settings
from .tools import Tools
from .url_validation import ValidURL

class YouTubeMedia:
    def __init__(self, url: str = None, uuidName: str = None) -> None:
        self.tools = Tools()
        self.url = url
        self.uuidName = uuidName
        self.yt_obj = None

        if self.url is not None:
            self.yt_obj = self.fetchData(self.url)

        self.info_format = {
            'id': 'id',
            'title': 'title',
            'original_url': 'url',
            'description': 'description',
            'duration': 'duration',
            'age_limit': 'age_limit',
            'thumbnail': 'thumbnail',
            'categories': 'categories',
            'tags': 'tags',
            'release_timestamp': 'release_timestamp',
            'name_author': 'uploader',
            'channel_id': 'channel_id',
            'channel_url': 'channel_url',
            'audio_protocol': 'protocol',
            'audio_bitrate': 'abr',
        }

        self.ydl_opts = {
            'extract_flat': True,
            'force_generic_extractor': True,
            'extract_info': True,
            'format': 'bestaudio/best',  # Wybór najlepszej jakości audio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Jeśli chcesz mp3 zamiast mp4
                'preferredquality': '192',  # Jakość audio
            }],
            'postprocessor_args': [
                '-acodec', 'libmp3lame',
                '-ar', '44100',
            ],
            'force_generic_extractor': True,
            'outtmpl': '%(id)s.%(ext)s',  # Nazwa pliku
            'download_archive': 'downloaded.txt',  # Plik śledzenia pobranych plików
            'quiet': False,  # Wyłączanie logów
            'extractor_args': {
                'youtube': {
                    'get_comments': False,  # Wyłączenie pobierania komentarzy
                },
            },
            'force_generic_extractor': True,
            'force_generic_format': True,
            'force_generic_extractors': True,
            'force_generic_formats': True,
            'force_generic_protocol': True,
            'force_generic_downloader': True,
            'youtube_include_dash_manifest': False,  # Wyłączenie manifestu DASH
            'skip_download': True,  # Pomijanie faktycznego pobierania plików
        }


    def fetchData(self, url) -> str:
        if not self.validURL(url):
            raise ValueError("Error loading urls. It's probably invalid, it doesn't exist")

        try:
            pass
        except:
            raise ValueError("Error loading urls. It's probably invalid, it doesn't exist")

    def downloadAudio(self, url: str = None, uuidName: str = None) -> str:
        if self.url is None and url is None:
            raise ValidationError("'url' parameter not passed")

        if self.uuidName is None and uuidName is None:
            raise ValidationError("'uuidName' parameter not passed")



    def downloadThumbnail(self, url: str = None, uuidName: str = None) -> str:
        if self.url is None and url is None:
            raise ValidationError("'url' parameter not passed")

        if self.uuidName is None and uuidName is None:
            raise ValidationError("'uuidName' parameter not passed")




    def infoURL(self, url: str = None) -> dict:
        if self.url is None and url is None:
            raise ValidationError("'url' parameter not passed.")

        if url is None:
            url = self.url

        if not ValidURL(url).is_valid:
            raise ValidationError("Invalid URL address, platform not supported.")

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            info = {key: info_dict[value] for key, value in self.info_format.items()}

        return json.dumps(ydl.sanitize_info(info))



YTFetch = YouTubeMedia()

if __name__ == "__main__":
    yt = YouTubeMedia().downloadAudio("https://music.youtube.com/watch?v=IxxstCcJlsc", "csadasfdsdgfdfgdfg")