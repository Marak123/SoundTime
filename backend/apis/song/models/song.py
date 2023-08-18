from django.db import models, transaction
from django.core.exceptions import ValidationError
import uuid
from datetime import datetime
from celery import shared_task

from apis.user.models import User
from apis.song.DlerMedia.YouTube import YouTubeMedia
from db.SoftDeleteModel import SoftDeleteModel, SoftDeleteManager

from .models import Author, Tags, Categories
from .fields import DownloadStatusField, ExtractorField


class SongManager(SoftDeleteManager):
    def create_by_url(self, **kwargs):
        return "Blad"
        if not 'url' in kwargs:
            raise ValidationError("URL is needed to create object as URL.")

        self.url = kwargs.pop('url')
        self.uuidName       = uuid.uuid4()

        obj_media = YouTubeMedia(self.url, self.uuidName.__str__())
        info        = obj_media.infoURL()
        # audio       = obj_media.downloadAudio()
        # thumbnail   = obj_media.downloadThumbnail()

        self.id              = self.uuidName
        self.user_added     = kwargs.pop('user_added',     None)

        # self.author = Author.objects.get_or_create(
        #                     name= ,
        #                     channelId= ,
        #                     channelUrl= ,
        #                     defaults={
        #                         "user_added": self.user_added
        #                     }
        #                 )


        obj = self.acreate(**{
            'id': self.id,
            
        })

        return obj


class Song(SoftDeleteModel):
    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)
    extractor  = ExtractorField()

    status = DownloadStatusField()
    created = models.DateTimeField(auto_now=True)
    # create_time = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Base Data
    url = models.URLField(unique=True)
    title = models.TextField(blank=True)
    duration = models.DurationField(default=0)
    release_timestamp = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    # Path Data
    audio_file = models.FileField(blank=True, null=True, editable=False)
    thumbnail_file = models.ImageField(blank=True, null=True, editable=False)
    url_thumbnail = models.URLField(blank=True)

    # Additional Information
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tags)
    categories = models.ManyToManyField(Categories)
    age_limit = models.IntegerField(default=0)
    audio_bitrate = models.IntegerField(null=True, blank=True)
    audio_protocol = models.CharField(null=True, blank=True)


    objects = SongManager()

    def __str__(self) -> str:
        return self.title