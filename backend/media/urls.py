from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import (
                media_audio_response,
                media_thumbnail_144_response,
                media_thumbnail_360_response,
                media_thumbnail_360_response,
                media_thumbnail_480_response,
                media_thumbnail_720_response,
                media_thumbnail_original_response
)

urlpatterns = [
    path('audio/<str:file_name>', media_audio_response, name="audio-transmit"),

    path('thumbnail/144/<str:file_name>', media_thumbnail_144_response, name="thumbnail-144p-transmit"),
    path('thumbnail/360/<str:file_name>', media_thumbnail_360_response, name="thumbnail-360p-transmit"),
    path('thumbnail/480/<str:file_name>', media_thumbnail_480_response, name="thumbnail-480p-transmit"),
    path('thumbnail/720/<str:file_name>', media_thumbnail_720_response, name="thumbnail-720p-transmit"),
    path('thumbnail/original/<str:file_name>', media_thumbnail_original_response, name="thumbnail-original-transmit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)