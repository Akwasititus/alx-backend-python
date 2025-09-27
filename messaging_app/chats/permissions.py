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
    Allow only authenticated users who are participants
    of the conversation to access messages.
    """

    def has_permission(self, request, view):
        # User must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        `obj` is expected to be either a Conversation or a Message
        with a `.conversation` attribute.
        """
        conversation = getattr(obj, "conversation", obj)
        return conversation.participants.filter(id=request.user.id).exists()