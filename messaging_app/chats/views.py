# from rest_framework import viewsets, status, filters
# from .models import User, Conversation, Message
# from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsParticipantOfConversation
from .models import Message
from .serializers import MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing conversations and creating new ones
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Only return messages for the given conversation_id if the
        current user is a participant. Otherwise, return 403.
        """
        conversation_id = self.kwargs.get("conversation_id")
        conversation = Conversation.objects.filter(id=conversation_id).first()
        if conversation and conversation.participants.filter(id=self.request.user.id).exists():
            return Message.objects.filter(conversation_id=conversation_id)
        # Explicitly return 403 Forbidden if not a participant
        self.permission_denied(
            self.request,
            message="You are not a participant of this conversation.",
            code=status.HTTP_403_FORBIDDEN,
        )
        