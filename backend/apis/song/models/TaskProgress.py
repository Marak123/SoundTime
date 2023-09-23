from django.db import models, transaction
import uuid

from apis.user.models import User
from db.SoftDeleteModel import SoftDeleteModel

class DownloadProgress(SoftDeleteModel):
    CODE_QUEUED = 0
    CODE_DOWNLOADING = 1
    CODE_FINISHED = 2
    CODE_ERROR = 3

    STATUS_CHOICES = (
        (CODE_QUEUED, 'queued', 'Queued'),
        (CODE_DOWNLOADING, 'downloading', 'Downloading'),
        (CODE_FINISHED, 'finished', 'Finished'),
        (CODE_ERROR, 'error', 'Error'),
    )

    id = models.UUIDField(unique=True, auto_created=True, blank=False, null=False, editable=False, db_index=True, primary_key=True, default=uuid.uuid4)

    created     = models.DateTimeField(auto_now=True)
    updated     = models.DateTimeField(auto_now_add=True)
    user_added  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    """"
        Stores information about the status of adding an object to the system.
        Possible options:
            - Queued (id = 0)       = waiting in queue to be added (download)
            - Downloading (id = 1)  = downloading
            - Finished (id = 2)     = additions completed
            - Error (id = 3)        = there was a problem adding

        Additional information to the field:
            0. Queued:
                - queue_position            = position in the queue
                - estimated_wait_time       = approximate waiting time
            1. Downloading
                - download_progress         = download progress (in percent, int)
                - estimated_wait_time       = approximate waiting time
            2. Finished
                - download_time             = final download time length
            3. Error
                - error_details             = information about the error that occurred
    """

    status = models.IntegerField(default=None, null=True, blank=True)

    def set_status(self, value):
        if isinstance(value, str):
            for code, choice, pname in self.STATUS_CHOICES:
                if value == choice or value == pname:
                    self.status = code
                    break
            else:
                raise ValueError("Invalid choice.")
        else:
            self.status = value

    def get_status(self):
        for code, choice, pname in self.STATUS_CHOICES:
            if self.status == code:
                return choice
        return None

    def get_status_p(self):
        for code, choice, pname in self.STATUS_CHOICES:
            if self.status == code:
                return pname
        return None

    status_name         = property(get_status, set_status)
    status_pname        = property(get_status_p, set_status)

    queue_position      = models.IntegerField(null=True, blank=True, default=None)
    download_progress   = models.FloatField(null=True, blank=True, default=None)
    estimated_wait_time = models.FloatField(null=True, blank=True, default=None)
    download_time       = models.FloatField(null=True, blank=True, default=None)
    error_details       = models.CharField(null=True, blank=True, default=None)