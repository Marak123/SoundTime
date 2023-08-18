from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from .models.models import Author
from .models.song import Song


class SongSerializer(serializers.ModelSerializer):
    url = serializers.URLField(
        required=True
    )  # , validators=[UniqueValidator(queryset=Song.objects.all())])

    class Meta:
        model = Song
        fields = [
            "id",
            "status",
            "extractor",
            "url",
            "title",
            "release_timestamp",
            "author",
            "url_thumbnail",
            "description",
            "tags",
            "categories",
            "age_limit",
            "audio_bitrate",
            "audio_protocol",
            "created",
            "updated",
            "duration",
            "user_added",
            "audio_file",
            "thumbnail_file",
        ]
        read_only_field = [
            "id",
            "created",
            "updated",
            "duration",
            "author",
            "audio_file",
            "thumbnail_file",
            "status",
            "extractor",
            "user_added",
            "url",
            "audio_bitrate",
            "audio_protocol",
        ]
        required = ["url"]
        # allow_null = ['title', 'date_release', 'author', 'url_thumbnail', 'description', 'rating', 'keywords']
        # depth = 1

    def validate_url(self, data):
        try:
            raise serializers.ValidationError(
                {
                    "error_message": "Object with this URL exists.",
                    "existing_object": SongSerializer(Song.objects.get(url=data)).data,
                }
            )
        except Song.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        song = Song.objects.create_by_url(**validated_data)
        # song.save()

        return song


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"
