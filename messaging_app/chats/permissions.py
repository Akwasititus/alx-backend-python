# from rest_framework.permissions import BasePermission
from rest_framework import permissions  # ✅ required import


class IsOwner(permissions.BasePermission):
    """
    Allow access only if the requesting user owns the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

