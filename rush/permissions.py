from rest_framework import permissions
from rush.models import User


class UserObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not isinstance(obj, User):
            obj = obj.user
        return request.user == obj
