from django.db import models, transaction
from django.core.exceptions import ValidationError
import uuid
from datetime import timedelta

from apis.user.models import User
from db.SoftDeleteModel import SoftDeleteModel, SoftDeleteManager

from .models import Author, Tags, Categories, Album
from .TaskProgress import DownloadProgress


class SongManager(SoftDeleteManager):
    def delete(self, *args, **kwargs):
        with transaction.atomic():
            super().delete(*args, **kwargs

)
    # def create_by_url(self, **kwargs):
    #     if not 'url' in kwargs:
    #         raise ValidationError("URL is needed to create object as URL.")

    #     self.url = kwargs.pop('url')
    #     self.uuidName = uuid.uuid4()

    #     try:
    #         self.info = Media.info(self.url)
    #     except ValueError as e:
    #         raise ValidationError(e)

    #     self.user_added = User.objects.get(pk=kwargs.pop('user_added', None))

    #     self.author = Author.objects.get_or_create(
    #                         name= self.info['name_author'],
    #                         channelId= self.info['channel_id'],
    #                         channelUrl= self.info['channel_url'],
    #                         defaults={
    #                             "user_added": self.user_added
    #                         }
    #                     )[0]

    #     self.album = Album.objects.get_or_create(
    #                         album= self.info['album'],
    #                         artist= self.info['artist'],
    #                         defaults={
    #                             "user_added": self.user_added
    #                         }
    #                     )[0]

    #     self.release_date = self.info['release_date']

    #     if len(self.release_date) == 8:
    #         self.release_date = f"{self.release_date[0:3]}-{self.release_date[4:5]}-{self.release_date[6:7]}"

    #     obj = Song.objects.create(**{
    #         'id':               self.uuidName,
    #         'extractor_name':   self.info.get('extractor', None),
    #         'user_added':       self.user_added,

    #         'url':              self.url,
    #         'title':            self.info.get('title', None),
    #         'duration':         timedelta(seconds=self.info.get('duration', 0)),
    #         'release_date':     self.release_date,
    #         'author':           self.author,

    #         'url_thumbnail':    self.info.get('url_thumbnail', None),

    #         'description':      self.info.get('description', None),
    #         'album':            self.album,
    #         'age_limit':        self.info.get('age_limit', None),

    #         'audio_bitrate':    self.info.get('audio_bitrate', None),
    #         'audio_protocol':   self.info.get('audio_protocol', None),
    #         'audio_extension':  self.info.get('audio_extension', None),

    #         # 'status':           Song.CODE_QUEUED,
    #         'download_progress': DownloadProgress.objects.create(id=self.uuidName),
    #     })

    #     obj.categories.set([ Categories.objects.get_or_create(name=cn, defaults={
    #                             "user_added": self.user_added
    #                         })[0] for cn in self.info['categories'] ])

    #     obj.tags.set([ Tags.objects.get_or_create(name=tn, defaults={
    #                             "user_added": self.user_added
    #                         })[0] for tn in self.info['tags'] ])


    #     try:
    #         Media.download(self.url, self.id.__str__())
    #     except Exception as e:
    #         self.hard_delete()

    #         raise ValidationError({
    #             "error_message": str(e)
    #         })

    #     return obj



class Song(SoftDeleteModel):
    CODE_FILE = 0
    CODE_YOUTUBE = 1
    CODE_SOUNDCLOUD = 2
    CODE_SPOTIFY = 3
    CODE_VIMEO = 4

    EXTRACTOR_CHOICES = (
        (CODE_FILE, 'file', 'File'),
        (CODE_YOUTUBE, 'youtube', 'YouTube'),
        (CODE_SOUNDCLOUD, 'soundcloud', 'SoundCloud'),
        (CODE_SPOTIFY, 'spotify', 'Spotify'),
        (CODE_VIMEO, 'vimeo', 'Vimeo'),
    )


    # CODE_QUEUED = 0
    # CODE_DOWNLOADING = 1
    # CODE_FINISHED = 2
    # CODE_ERROR = 3

    # STATUS_CHOICES = (
    #     (CODE_QUEUED, 'queued', 'Queued'),
    #     (CODE_DOWNLOADING, 'downloading', 'Downloading'),
    #     (CODE_FINISHED, 'finished', 'Finished'),
    #     (CODE_ERROR, 'error', 'Error'),
    # )

    id              = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)

    created         = models.DateTimeField(auto_now=True)
    # create_time = models.DateTimeField(auto_now=True)
    updated         = models.DateTimeField(auto_now_add=True)
    user_added      = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Base Data
    url             = models.URLField(unique=True)
    title           = models.TextField(blank=True)
    duration        = models.DurationField(default=0)
    release_date    = models.DateTimeField(auto_now=True)
    author          = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    # Path Data
    audio_file      = models.FileField(blank=True, null=True, editable=False, max_length=255)
    thumbnail_file  = models.ImageField(blank=True, null=True, editable=False, max_length=255)
    url_thumbnail   = models.URLField(blank=True)

    # Additional Information
    description     = models.TextField(null=True, blank=True)
    tags            = models.ManyToManyField(Tags, blank=True)
    categories      = models.ManyToManyField(Categories, blank=True)
    album           = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    age_limit       = models.IntegerField(default=0)

    audio_bitrate   = models.IntegerField(null=True, blank=True)

    download_progress = models.ForeignKey(DownloadProgress, on_delete=models.CASCADE, null=True, blank=True)

    # objects = SongManager()

    def __str__(self) -> str:
        return self.title

    """
        Information handler about how to deliver the audio file, etc.
        Possible options are:
            - Files         = uploading files yourself
            - YouTube       = download downloaded from youtube.com
            - SoundCloud    = download downloaded from soundcloud.com
            - Spotify       = download downloaded from spotify.com
            - Vimeo         = download downloaded from vimeo.com
    """

    def set_extractor(self, value):
        if isinstance(value, str):
            for code, choice, pname in self.EXTRACTOR_CHOICES:
                if value == choice or value == pname:
                    self.extractor = code
                    break
            else:
                raise ValueError("Invalid choice.")
        else:
            self.extractor = value

    def get_extractor(self):
        for code, choice, pname in self.EXTRACTOR_CHOICES:
            if self.extractor == code:
                return choice
        return None

    def get_extractor_p(self):
        for code, choice, pname in self.EXTRACTOR_CHOICES:
            if self.extractor == code:
                return pname
        return None

    """Main field storing id (int) information"""
    extractor = models.IntegerField(default=None, null=True, blank=True)

    """Sub field, field dependent `extractor` returns the base name depending on the value"""
    extractor_name = property(get_extractor, set_extractor,
                            doc="""Sub field, field dependent `extractor` returns the base name depending on the value""")

    """Sub field, field dependent `extractor` returns a nice looking name depending on the value"""
    extractor_pname = property(get_extractor_p, set_extractor,
                            doc="""Sub field, field dependent `extractor` returns a nice looking name depending on the value""")



    # """"
    #     Stores information about the status of adding an object to the system.
    #     Possible options:
    #         - Queued (id = 0)       = waiting in queue to be added (download)
    #         - Downloading (id = 1)  = downloading
    #         - Finished (id = 2)     = additions completed
    #         - Error (id = 3)        = there was a problem adding

    #     Additional information to the field:
    #         0. Queued:
    #             - queue_position            = position in the queue
    #             - estimated_wait_time       = approximate waiting time
    #         1. Downloading
    #             - download_progress         = download progress (in percent, int)
    #             - estimated_wait_time       = approximate waiting time
    #         2. Finished
    #             - download_time             = final download time length
    #         3. Error
    #             - error_details             = information about the error that occurred
    # """

    # status = models.IntegerField(default=None, null=True, blank=True)

    # def set_status(self, value):
    #     if isinstance(value, str):
    #         for code, choice, pname in self.STATUS_CHOICES:
    #             if value == choice or value == pname:
    #                 self.status = code
    #                 break
    #         else:
    #             raise ValueError("Invalid choice.")
    #     else:
    #         self.status = value

    # def get_status(self):
    #     for code, choice, pname in self.STATUS_CHOICES:
    #         if self.status == code:
    #             return choice
    #     return None

    # def get_status_p(self):
    #     for code, choice, pname in self.STATUS_CHOICES:
    #         if self.status == code:
    #             return pname
    #     return None

    # status_name         = property(get_status, set_status)
    # status_pname        = property(get_status_p, set_status)

    # queue_position      = models.IntegerField(null=True, blank=True, default=None)
    # download_progress   = models.FloatField(null=True, blank=True, default=None)
    # estimated_wait_time = models.FloatField(null=True, blank=True, default=None)
    # download_time       = models.FloatField(null=True, blank=True, default=None)
    # error_details       = models.CharField(null=True, blank=True, default=None)