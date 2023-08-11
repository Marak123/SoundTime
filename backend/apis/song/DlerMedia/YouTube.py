from pytube import YouTube
import requests, os, re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from django.conf import settings
from .tools import Tools

class YouTubeMedia:
    def __init__(self, url: str = None, uuidName: str = None) -> None:
        self.tools = Tools()
        self.url = url
        self.uuidName = uuidName
        self.yt_obj = None

        if self.url is not None:
            self.yt_obj = self.fetchData(self.url)

    def validURL(self, url: str) -> bool:
        validate_url = URLValidator()

        try:
            validate_url(url)
        except ValidationError:
            raise ValidationError("Invalid URL")
            # return False

        if re.match(
            (
                r'(https?://)?(www\.|music\.)?'
                '(youtube|youtu|youtube-nocookie)\.(com|be)/'
                '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
            ),
            url
        ):
            r = requests.get("https://www.youtube.com/oembed?url=" + url)
            if r.status_code != 200:
                return False
        else:
            return False

        return True

    def fetchData(self, url) -> str:
        if not self.validURL(url):
            raise ValueError("Error loading urls. It's probably invalid, it doesn't exist")

        try:
            return YouTube(
                    url,
                    # on_progress_callback=self.onProgressCallback if self.onProgressCallback is not None else None,
                    # on_complete_callback=self.onCompleteCallback if self.onCompleteCallback is not None else None,
                    use_oauth=True, allow_oauth_cache=True
                )
        except:
            raise ValueError("Error loading urls. It's probably invalid, it doesn't exist")

    def downloadAudio(self, url: str = None, uuidName: str = None) -> str:
        if self.url is None and url is None:
            raise ValidationError("'url' parameter not passed")

        if self.uuidName is None and uuidName is None:
            raise ValidationError("'uuidName' parameter not passed")

        if url is None:
            yt_obj = self.yt_obj
        else:
            yt_obj = self.fetchData(url)

        if uuidName is None:
            uuidName = self.uuidName

        stream = yt_obj.streams.filter(only_audio=True).order_by('abr').desc().first()
        pathNameToDownload = f"{ uuidName }.{ stream.subtype }"

        try:
            stream.download(
                output_path=settings.MEDIA_AUDIO,
                filename=pathNameToDownload
            )
        except ValueError:
            raise ValueError(f"Error downloading audio from url { url }")

        return pathNameToDownload

    def downloadThumbnail(self, url: str = None, uuidName: str = None) -> str:
        if self.url is None and url is None:
            raise ValidationError("'url' parameter not passed")

        if self.uuidName is None and uuidName is None:
            raise ValidationError("'uuidName' parameter not passed")

        if url is None:
            yt_obj = self.yt_obj
        else:
            yt_obj = self.fetchData(url)

        if uuidName is None:
            uuidName = self.uuidName

        # with open(pathNameToThumbnail, 'wb') as f:
        #     f.write(requests.get(yt.thumbnail_url).content)

        fileName = uuidName + ".jpg"

        self.tools.cropByteImage(
                        byte_image=requests.get(yt_obj.thumbnail_url, stream=True).raw,
                        name_file=os.path.join(settings.MEDIA_THUMBNAIL, fileName)
                    )

        return fileName

    def infoURL(self, url: str = None) -> dict:
        if self.url is None and url is None:
            raise ValidationError("'url' parameter not passed")

        if url is None:
            yt_obj = self.yt_obj
        else:
            yt_obj = self.fetchData(url)

        return {
            'title':         yt_obj.title,
            'duration':      yt_obj.length,
            'author':        yt_obj.author,
            'thumbnail_url': yt_obj.thumbnail_url,
            'publish_date':  yt_obj.publish_date.__str__(),
            'description':   yt_obj.description,
            'rating':        yt_obj.rating,
            'views':         yt_obj.views,
            'keywords':      yt_obj.keywords,
            'channel_id':    yt_obj.channel_id,
            'channel_url':   yt_obj.channel_url
        }

YTFetch = YouTubeMedia()

if __name__ == "__main__":
    yt = YouTubeMedia().downloadAudio("https://music.youtube.com/watch?v=IxxstCcJlsc", "csadasfdsdgfdfgdfg")