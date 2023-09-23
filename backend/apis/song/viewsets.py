from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


from .serializers import SongSerializer, AuthorSerializer
from .models.models import Author
from .models.Song import Song
from apis.viewsets import SoftDeleteViewSet

class SongViewSet(SoftDeleteViewSet):
    model = Song
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    # def list(self, request):
    #     return Response(self.serializer_class(self.queryset, many=True).data)

    # def retrieve(self, request, pk=None):
    #     song = get_object_or_404(self.queryset, pk=pk)
    #     serializer = self.serializer_class(song)
    #     return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data | {'user_added': request.user.pk})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @action(methods=['GET'], detail=True)
    # def 


class AuthorViewSet(SoftDeleteViewSet):
    model = Author
    serializer_class = AuthorSerializer
    permission_classes = [
        IsAuthenticated,
    ]