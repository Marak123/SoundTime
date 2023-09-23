from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from core import settings

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication


import os

from .ranged_file_response.ranged_fileresponse import RangedFileResponse




@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def media_audio_response(request, file_name):
    media_root = os.path.join(settings.OUTPUT_AUDIO_PATH, file_name)
    response = RangedFileResponse(request,open(media_root, 'rb'), content_type='audio/mpeg')
    # response['Content-Disposition'] = 'attachment; filename="%s"' % file_name

    return response

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def media_thumbnail_144_response(request, file_name):
    return media_fileresponse(file_name, '144')

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def media_thumbnail_360_response(request, file_name):
    return media_fileresponse(file_name, '360')

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def media_thumbnail_480_response(request, file_name):
    return media_fileresponse(file_name, '480')

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def media_thumbnail_720_response(request, file_name):
    return media_fileresponse(file_name, '720')

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def media_thumbnail_original_response(request, file_name):
    return media_fileresponse(file_name, 'ORIGINAL')



def media_fileresponse(file_name: str, resolution: str):
    media_root = os.path.join(settings.OUTPUT_IMAGE_PATH, file_name, settings.THUMBNAIL_NAME_RESOLUTION[resolution.upper()])

    return FileResponse(open(media_root, 'rb'), content_type='image/webp')