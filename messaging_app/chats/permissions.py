# from rest_framework.permissions import BasePermission
from rest_framework import permissions  # ✅ required import
from .models import Conversation 


class IsOwner(permissions.BasePermission):
    """
    Allow access only if the requesting user owns the object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only authenticated participants to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Explicitly check for PUT, PATCH, DELETE (update & delete) and GET/POST.
        """
        if request.method in ["PUT", "PATCH", "DELETE", "GET", "POST"]:
            conversation = getattr(obj, "conversation", obj)
            return conversation.participants.filter(id=request.user.id).exists()
        return False
        