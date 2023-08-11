from rest_framework.routers import SimpleRouter
from .user.viewsets import UserViewSet, GroupViewSet
from .auth.viewsets import LoginViewSet, RefreshViewSet, LogoutViewSet
from .song.viewsets import *
# from core.api.views import ListAllPathAPI
from django.urls import path, include


routes = SimpleRouter()

# AUTHENTICATION
routes.register(r'auth/login', LoginViewSet, basename='auth-login')
routes.register(r'auth/logout', LogoutViewSet, basename='auth-logout')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# USER
routes.register(r'users', UserViewSet, basename='users')
routes.register(r'groups', GroupViewSet, basename='groups')
routes.register(r'songs', SongViewSet, basename='songs')
routes.register(r'authors', AuthorViewSet, basename='author')


urlpatterns = routes.urls + [
    
]
