from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


from .serializers import UserSerializer, GroupSerializer
from .models import User, Group
from .permissions import IsAdminGroup


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]

    def list(self, request):
        return Response(
            self.serializer_class(self.queryset, many=True).data
        )

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": serializer.data,
            "refresh": str(refresh),
            "token": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminGroup,]

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        group = get_object_or_404(self.queryset, pk=pk)
        # admin_user = get_object_or_404(User, pk=group.is_admin.id)

        # Dodajemy nowe dane do obiektu "group"
        # group.is_admin_user = {
        #     "id": admin_user.id,
        #     "username": admin_user.username,
        #     "email": admin_user.email,
        #     "is_active": admin_user.is_active,
        #     "created": admin_user.created,
        #     "updated": admin_user.updated
        # }

        serializer = self.serializer_class(group)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=True, url_path="fulldata", url_name="fulldata")
    def full_data(self, request, pk=None):
        return Response("cos")