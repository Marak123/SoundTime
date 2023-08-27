from django.db import models, transaction
from django.core.exceptions import ValidationError
import uuid
from datetime import datetime
from celery import shared_task

from apis.user.models import User
from apis.song.DlerMedia.YouTube import YouTubeMedia
from db.SoftDeleteModel import SoftDeleteModel, SoftDeleteManager
from .fields import DownloadStatusField, ExtractorField

class Author(SoftDeleteModel):
    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField()
    channelId = models.CharField(max_length=200)
    channelUrl = models.URLField()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

class Categories(SoftDeleteModel):
    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

class Tags(SoftDeleteModel):
    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)
    name = models.CharField()

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.name

class Album(SoftDeleteModel):
    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)

    album = models.CharField(null=True, blank=True)
    artist = models.CharField(null=True, blank=True)

    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    user_added = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
