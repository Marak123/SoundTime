from django.db import models, transaction
from django.core.exceptions import ValidationError
import uuid
from datetime import datetime

from apis.user.models import User
from apis.song.DlerMedia.YouTube import YTFetch, YouTubeMedia
from db.SoftDeleteModel import SoftDeleteModel, SoftDeleteManager


class Author(SoftDeleteModel):
    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)
    name = models.TextField()
    channelId = models.CharField(max_length=200)
    channelUrl = models.URLField()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name


class SongManager(SoftDeleteManager):
    def create_by_url(self, **kwargs):
        if not 'url' in kwargs:
            raise ValidationError("URL is needed to create object as URL.")

        self.url = kwargs.pop('url')
        self.uuidName       = uuid.uuid4()

        yt_media = YouTubeMedia(self.url, self.uuidName.__str__())
        yt_info        = yt_media.infoURL()
        yt_audio       = yt_media.downloadAudio()
        yt_thumbnail   = yt_media.downloadThumbnail()

        self.id              = self.uuidName
        self.path_audio      = yt_audio
        self.path_thumbnail  = yt_thumbnail
        self.user_added     = kwargs.pop('user_added',     None)

        self.author = Author.objects.get_or_create(
                            name=yt_info['author'],
                            channelId=yt_info['channel_id'],
                            channelUrl=yt_info['channel_url'],
                            defaults={
                                "user_added": self.user_added
                            }
                        )

        self.url_thumbnail  = yt_info['thumbnail_url']
        self.duration       = yt_info['duration']
        self.title          = kwargs.pop('title',          yt_info['title'])
        self.date_release   = kwargs.pop('date_release',   datetime.strptime(yt_info['publish_date'], "%Y-%m-%d %H:%M:%S"))
        self.description    = kwargs.pop('description',    yt_info['description'])
        self.rating         = kwargs.pop('rating',         yt_info['rating'])
        self.keywords       = kwargs.pop('keywords',       yt_info['keywords'])

        # obj = self.model(**kwargs)
        # # self._for_write = True
        # obj.save(force_insert=True, using=self.db)

        obj = self.acreate(**{
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'author': self.author,
            'duration': self.duration,
            'path_audio': self.path_audio,
            'path_thumbnail': self.path_thumbnail,
            'url_thumbnail': self.url_thumbnail,
            'date_release': self.date_release,
            'description': self.description,
            'rating': self.rating,
            'keywords': self.keywords,
            'user_added': self.user_added,
        })

        return obj



class Song(SoftDeleteModel):
    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Base Data
    url = models.URLField(unique=True)
    title = models.TextField(blank=True)
    duration = models.IntegerField(default=0)
    date_release = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    # Path Data
    path_audio = models.CharField(max_length=100, blank=True, null=True, editable=False)
    path_thumbnail = models.CharField(max_length=100, blank=True, null=True, editable=False)
    url_thumbnail = models.URLField(blank=True)

    # Additional Information
    description = models.TextField(null=True, blank=True)
    rating = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)


    objects = SongManager()

    def __str__(self) -> str:
        return self.title