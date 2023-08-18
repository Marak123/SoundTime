from typing import Any
from django.db import models
from django.utils.translation import gettext_lazy as _

"""
    Status:

    - queued - w kolejce czeka na pobranie
    - downloading (lub coś takiego, jeżeli masz lepszą nazwę) - w trakcie pobierania
    - finish - zakończone pobieranie
    - error - błąd pobierania

    Odnośnie tych statusów to powinno możliwe być pobranie dodatkowych informacji takich jak:

    - do statusu `queued`, numer w kolejce
    - do statusu `downloading` (lub coś takiego), procent pobrania i czas oczekiwania przybliżony
    - do statusu `finish`, czas pobierania i wielkosc pliku
    - do statusu `error`, błąd jaki wystąpił, szczegółowe informacje

    Dodatkowo każdy z tych statusów powninien mieć własny krótki numer identyfikacji tzn.

    - queued to 1
    - downloading to 2
    - finish to 3
    - error to 4

"""


class DownloadStatusField(models.IntegerField):

    empty_strings_allowed = False
    default_error_messages = {
        "invalid": _("“%(value)s” this field does not take this value."),
    }
    description = _("Download status value")

    CODE_QUEUED = 1
    CODE_DOWNLOADING = 2
    CODE_FINISHED = 3
    CODE_ERROR = 4

    STATUS_CHOICES = (
        (CODE_QUEUED, 'Queued'),
        (CODE_DOWNLOADING, 'Downloading'),
        (CODE_FINISHED, 'Finished'),
        (CODE_ERROR, 'Error'),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.choices = self.STATUS_CHOICES
        self.default = 0
        self.status = 0

        self.queue_position = None
        self.download_progress = None
        self.estimated_wait_time = None
        self.download_time = None
        self.error_details = None

    def __str__(self) -> str:
        return self.STATUS_CHOICES[self.value_from_object(self)][1]

    @property
    def status_code(self):
        return self.STATUS_CHOICES[self.value_from_object(self)][0]

    @property
    def status_name(self) -> str:
        return self.STATUS_CHOICES[self.value_from_object(self)][1]

    @property
    def status_description(self) -> str:
        return self.STATUS_CHOICES[self.value_from_object(self)][2]




class ExtractorField(models.IntegerField):
    empty_strings_allowed = False
    default_error_messages = {
        "invalid": _("“%(value)s” this field does not take this value."),
    }
    description = _("Platform extractor name")

    CODE_FILE= 1
    CODE_YOUTUBE = 2
    CODE_SOUNDCLOUD = 3
    CODE_SPOTIFY = 4
    CODE_VIMEO = 5

    EXTRACTOR_CHOICES = (
        (CODE_FILE, 'File'),
        (CODE_YOUTUBE, 'YouTube'),
        (CODE_SOUNDCLOUD, 'SoundCloud'),
        (CODE_SPOTIFY, 'Spotify'),
        (CODE_VIMEO, 'Vimeo'),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.choices = self.EXTRACTOR_CHOICES
        self.default = 0
        self.extractor = 0

    def __str__(self) -> str:
        return self.EXTRACTOR_CHOICES[self.value_from_object(self)][1]

    @property
    def extractor_name(self) -> str:
        return self.EXTRACTOR_CHOICES[self.value_from_object(self)][1]

    @property
    def extractor_description(self) -> str:
        return self.EXTRACTOR_CHOICES[self.value_from_object(self)][2]
