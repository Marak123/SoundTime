from typing import Any
from rest_framework import viewsets, status, filters, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

class SoftDeleteViewSet(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    model = None


    def __set_queryset_not_deleted(self):
        assert self.model is not None, (
            "'%s' should either include a `model` attribute"
            % self.__class__.__name__
        )

        assert self.model.objects is not None, "The `model` attribute should be the `SoftDeleteModel`"

        self.queryset = self.model.objects.all()

    def __set_queryset_deleted(self):
        assert self.model is not None, (
            "'%s' should either include a `model` attribute"
            % self.__class__.__name__
        )

        assert self.model.all_objects is not None, "The `model` attribute should be the `SoftDeleteModel`"

        self.queryset = self.model.all_objects.only_deleted()

    def __set_queryset_all(self):
        assert self.model is not None, (
            "'%s' should either include a `model` attribute"
            % self.__class__.__name__
        )

        assert self.model.all_objects is not None, "The `model` attribute should be the `SoftDeleteModel`"

        self.queryset = self.model.all_objects.all()



    def create(self, request, *args, **kwargs):
        """
            Create new object
        """

        self.__set_queryset_not_deleted()
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
            List all not deleted objects
        """

        self.__set_queryset_not_deleted()
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
            Retrive not deleted objects
        """

        self.__set_queryset_not_deleted()
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
            Update not deleted objects
        """

        self.__set_queryset_not_deleted()
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
            Soft remove not deleted object
        """

        self.__set_queryset_not_deleted()
        instance = self.get_object()
        instance.delete(deleted_uuid=request.user.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(methods=['GET'], detail=False, url_path='deleted', url_name='only_deleted_objects', permission_classes=[IsAdminUser])
    def only_deleted(self, request, *args, **kwargs):
        """
            List all deleted objects

            `IsAdminUser` permission required
        """

        self.__set_queryset_deleted()
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='all', url_name='all_objects', permission_classes=[IsAdminUser])
    def all_objects(self, request, *args, **kwargs):
        """
            List all objects, deleted and not deleted

            `IsAdminUser` permission required
        """

        self.__set_queryset_all()
        return super().list(request, *args, **kwargs)


    @action(methods=['DELETE'], detail=True, url_path='hard_delete', url_name='hard_delete', permission_classes=[IsAdminUser])
    def hard_delete(self, request, *args, **kwargs):
        """
            Hard delete object, deleted and not deleted

            `IsAdminUser` permission required
        """

        self.__set_queryset_all()
        instance = self.get_object()
        instance.hard_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(methods=['PATCH'], detail=True, url_path='restore', url_name='restore_deleted', permission_classes=[IsAdminUser])
    def restore_deleted(self, request, *args, **kwargs):
        """
            Restore delete object, deleted and not deleted

            `IsAdminUser` permission required
        """

        self.__set_queryset_deleted()
        instance = self.get_object()
        instance.undelete()
        return Response(status=status.HTTP_202_ACCEPTED)