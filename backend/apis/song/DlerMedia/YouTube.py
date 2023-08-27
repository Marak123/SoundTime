from pytube import YouTube
import requests, os, re, yt_dlp, json
from PIL import Image
from celery import shared_task

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# from django.conf import settings
from core.settings import MEDIA_ROOT
from .tools import Tools
from .url_validation import ValidURL

class YouTubeMedia:
    outputPathSong = f'{MEDIA_ROOT}/songs/'
    outputPathTemp = f'{MEDIA_ROOT}/temp/'
    info_format = {
        'audio_id': 'id',
        'audio_protocol': 'protocol',
        'audio_bitrate': 'abr',
        'audio_extension': 'audio_ext',
        'extractor': 'extractor',

        'title': 'title',
        'url': 'original_url',
        'description': 'description',
        'duration': 'duration',
        'age_limit': 'age_limit',
        'url_thumbnail': 'thumbnail',
        'categories': 'categories',
        'tags': 'tags',
        'release_date': 'upload_date', # YYYYMMDD

        'name_author': 'uploader',
        'channel_id': 'channel_id',
        'channel_url': 'channel_url',
        'channel_name': 'channel',

        'album': 'album',
        'artist': 'artist',
        'track': 'track',
    }

    def __init__(self, obj = None) -> None:
        self.tools = Tools()
        self.songObject = obj
        self.resolution = [(256, 144), (640, 360), (720, 480), (1280, 720)]

        self.ydl_opts = {
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
            'progress_hooks': [self.progress_hooks],
            'paths': {
                'home': self.outputPathSong,
                'temp': self.outputPathTemp,
            },
            # 'outtmpl': '%(id)s/%(id)s.%(ext)s',
            'writethumbnail': True,
            'quiet': True,
        }


    def progress_hooks(self, info):
        if info['status'] == "downloading":

            self.songObject.estimated_wait_time = float(info['eta']) if info.get('eta', None) is not None else None
            self.songObject.download_time       = float(info['elapsed']) if info.get('elapsed', None) is not None else None
            self.songObject.download_progress   = float(info['downloaded_bytes'] / info['total_bytes_estimate'])  if info.get('downloaded_bytes', None) is not None and info.get('total_bytes_estimate', None) is not None else None

        elif info['status'] == "finished":

            self.songObject.status = self.songObject.CODE_FINISHED

            self.songObject.estimated_wait_time = float(info['eta']) if info.get('eta', None) is not None else None
            self.songObject.download_time       = float(info['elapsed']) if info.get('elapsed', None) is not None else None

            self.songObject.audio_file          = info.get("info_dict", dict).get("filename", None)


            thumbnails = info.get("info_dict", dict).get('thumbnails', None)
            best_thumbnail = max(thumbnails, key=lambda thumbnail: thumbnail.get('width', 0) * thumbnail.get('height', 0))
            path_elements = best_thumbnail.get('filepath', "").split("/")
            path_elements = "/".join(path_elements[-2:])

            self.songObject.thumbnail_file =    f'{self.outputPathSong}{path_elements}'

            # print(json.dumps(info))

        elif info['status'] == "error":
            self.songObject.status = self.songObject.CODE_ERROR

    @classmethod
    def infoURL(self, url: str) -> dict:
        if not ValidURL(url).is_valid:
            raise ValidationError("Invalid URL address, platform not supported.")

        with yt_dlp.YoutubeDL({
            'format': 'bestaudio/best',
            'quiet': True,
        }) as ydl:
            info_dict = ydl.extract_info(url, download=False)

        return {
            key: (info_dict[value] if value in info_dict else None) for key, value in self.info_format.items()
        }



    @shared_task
    def download(self, url: str, uuidName: str) -> str:
        if self.songObject is None:
            raise ValidationError('Song object is not passed')

        if not ValidURL(url).is_valid:
            raise ValidationError("`url` is not valid or the platform is not supported.")

        yt_opt = self.ydl_opts | {'outtmpl': f'{uuidName}/{uuidName}.%(ext)s'}
        with yt_dlp.YoutubeDL(yt_opt) as ydl:
            self.songObject.status = self.songObject.CODE_DOWNLOADING

            dl = ydl.download(url)

        if dl:
            self.songObject.status = self.songObject.CODE_ERROR

        else:
            self.convertThumbnailRize(
                f'{self.outputPathSong}/{uuidName}/',
                self.songObject.thumbnail_file,
                self.resolution
            )

    def async_download(url: str, ydl_opt: dict):
        pass

    def convertThumbnailRize(self, outputPath: str, imagePath: str, finalResolution: list) -> str:
        image = Image.open(imagePath)

        for res in finalResolution:
            resized_image = image.resize(res)
            resized_image.save(f'{outputPath}thumbnail_{res[1]}p.webp')

        image.save(f'{outputPath}thumbnail_original.webp')

        self.songObject.thumbnail_file = f'{outputPath}thumbnail_original.webp'






# YTFetch = YouTubeMedia()

if __name__ == "__main__":
    yt = YouTubeMedia().downloadAudio("https://music.youtube.com/watch?v=IxxstCcJlsc", "csadasfdsdgfdfgdfg")