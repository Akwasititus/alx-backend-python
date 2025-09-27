from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Allow access only if the requesting user owns the object.
    Assumes the model has a `user` or `owner` field.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
