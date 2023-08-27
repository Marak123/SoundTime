from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from .models.models import Author, Tags, Categories, Album
from .models.song import Song
from apis.user.serializers import UserSerializer, UserSerializerField
from .DlerMedia.url_validation import ValidURL


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ['deleted']

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        exclude = ['deleted']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        exclude = ['deleted']

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        exclude = ['deleted']


class SongSerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    user_added = UserSerializerField()
    album = AlbumSerializer(required=False)
    tags = TagsSerializer(many=True, required=False)
    categories = CategoriesSerializer(many=True, required=False)
    author = AuthorSerializer(required=False)
    extractor = serializers.CharField(source='extractor_name', required=False)
    status = serializers.CharField(source='status_name', required=False)

    class Meta:
        model = Song
        read_only_field = [
            "id",
            "created",
            "updated",
            "duration",
            "author",
            "audio_file",
            "thumbnail_file",
            "status",
            "extractor_name",
            "user_added",
            "audio_bitrate",
            "audio_protocol",
            "audio_extension",
        ]
        exclude = ['deleted']
        required = ["url"]
        # allow_blank = ['album', 'tags', 'categories', 'author', 'extractor', 'status']
        depth = 1

    def validate_url(self, data):
        if not ValidURL(data).is_valid:
            print(data)
            raise serializers.ValidationError({
                "error_message": "The URL is not valid or the site is not supported"
            })

        try:
            e = serializers.ValidationError(
                {
                    "error_message": "The object with this URL existed but was deleted, restoring.",
                    "existing_object": SongSerializer(Song.all_objects.only_deleted().get(url=data)).data,
                }
            )

            Song.all_objects.only_deleted().get(url=data).undelete()

            raise e
        except Song.DoesNotExist:
            pass

        try:
            raise serializers.ValidationError(
                {
                    "error_message": "The object with this URL exists.",
                    "existing_object": SongSerializer(Song.objects.get(url=data)).data,
                }
            )
        except Song.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        song = Song.objects.create_by_url(**validated_data)
        print(song)
        # song.save()

        return song