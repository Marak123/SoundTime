from yt_dlp.utils import DownloadError
from PIL import Image

from django.core.exceptions import ValidationError

from .tools import Tools
from .platform_valid import ValidURL
from .platform_class import YouTube

class Media:
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

    @classmethod
    def info(self, url: str) -> dict:
        valid_url = ValidURL(url)

        if not valid_url.is_valid:
            raise ValidationError("Invalid URL address, platform not supported.")

        if valid_url.platform == 'youtube':
            try:
                info_dict = YouTube.info(url)
            except DownloadError:
                raise ValidationError("Failed to fetch media information.")

        return {
            key: (info_dict[value] if value in info_dict else None) for key, value in Media.info_format.items()
        }

    @classmethod
    def download(self, url: str, uuid: str) -> str:
        valid_url = ValidURL(url)

        if not valid_url.is_valid:
            raise ValidationError("Invalid URL address, platform not supported.")

        if valid_url.platform == 'youtube':
            return YouTube.download(url, uuid)

        return None