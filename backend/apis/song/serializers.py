from django.contrib.auth.models import Permission
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

import uuid
from datetime import timedelta

from .models.models import Author, Tags, Categories, Album
from .models.Song import Song
from .models.TaskProgress import DownloadProgress

from apis.user.models import User
from apis.user.serializers import UserSerializer, UserSerializerField

from apis.song.DlerMedia.media import Media
from apis.song.DlerMedia.platform_valid import ValidURL


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

class DownloadProgressSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status_name', required=False)

    class Meta:
        model = DownloadProgress
        exclude = ['deleted']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None and not value == 'null'}


class SongSerializer(serializers.ModelSerializer):
    url = serializers.URLField()
    user_added = UserSerializerField()
    album = AlbumSerializer(required=False)
    tags = TagsSerializer(many=True, required=False)
    categories = CategoriesSerializer(many=True, required=False)
    author = AuthorSerializer(required=False)
    download_progress = DownloadProgressSerializer(required=False)
    extractor = serializers.CharField(source='extractor_name', required=False)

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
        depth = 1

    def validate_url(self, data):
        if not ValidURL(data).is_valid:
            raise serializers.ValidationError({
                "error_message": "The URL is not valid or the site is not supported."
            })

        try:
            song = Song.all_objects.only_deleted().get(url=data)

            e = serializers.ValidationError({
                    "error_message": "The object with this URL existed but was deleted, restoring.",
                    "existing_object": SongSerializer(song).data,
                })

            song.undelete()

            raise e
        except Song.DoesNotExist:
            pass

        try:
            raise serializers.ValidationError({
                    "error_message": "The object with this URL exists.",
                    "existing_object": SongSerializer(Song.objects.get(url=data)).data,
                })
        except Song.DoesNotExist:
            pass

        return data


    def create(self, validated_data):
        try:

            url = validated_data.pop('url')

            try:
                info = Media.info(url)
            except ValueError as e:
                raise serializers.ValidationError(e)

            user_added = User.objects.get(pk=validated_data.pop('user_added', None))

            author = Author.objects.get_or_create(
                                name= info['name_author'],
                                channelId= info['channel_id'],
                                channelUrl= info['channel_url'],
                                defaults={
                                    "user_added": user_added
                                }
                            )[0]

            album = Album.objects.get_or_create(
                                album= info['album'],
                                artist= info['artist'],
                                defaults={
                                    "user_added": user_added
                                }
                            )[0]

            release_date = info['release_date']

            if len(release_date) == 8:
                release_date = f"{release_date[0:3]}-{release_date[4:5]}-{release_date[6:7]}"

            uuidName = uuid.uuid4()
            song = Song.objects.create(**{
                'id':               uuidName,
                'extractor_name':   info.get('extractor', None),
                'user_added':       user_added,

                'url':              url,
                'title':            info.get('title', None),
                'duration':         timedelta(seconds=info.get('duration', 0)),
                'release_date':     release_date,
                'author':           author,

                'url_thumbnail':    info.get('url_thumbnail', None),

                'description':      info.get('description', None),
                'album':            album,
                'age_limit':        info.get('age_limit', None),

                'audio_bitrate':    info.get('audio_bitrate', None),

                'download_progress': DownloadProgress.objects.create(
                    id=uuidName,
                    user_added=user_added,
                    status=DownloadProgress.CODE_QUEUED,
                ),
            })

            song.categories.set([ Categories.objects.get_or_create(name=cn, defaults={
                                    "user_added": user_added
                                })[0] for cn in info['categories'] ])

            song.tags.set([ Tags.objects.get_or_create(name=tn, defaults={
                                    "user_added": user_added
                                })[0] for tn in info['tags'] ])


            try:
                Media.download(url, uuidName.__str__())
            except Exception as e:
                song.hard_delete()

                raise serializers.ValidationError({
                    "error_message": str(e)
                })


        except ValueError as e:
            raise serializers.ValidationError({
                "error_message": str(e)
            })


        return song