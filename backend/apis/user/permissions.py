from rest_framework.permissions import BasePermission


class IsAdminGroup(BasePermission):
    def has_permission(self, request, view):
        # Wszystkim zalogowanym użytkownikom zezwalamy na dostęp do widoku listy grup.
        if view.action == 'list':
            return request.user.is_authenticated

        # Dla pozostałych akcji (retrieve, create, update, delete), wymagamy, aby użytkownik był administratorem grupy.
        return request.user.is_authenticated and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        # Jeśli użytkownik jest administratorem grupy (jest powiązany z polem is_admin),
        # zezwalamy na dostęp do konkretnego obiektu grupy.
        return request.user == obj.is_admin